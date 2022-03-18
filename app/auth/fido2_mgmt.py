import logging

from fido2 import cbor
from fido2.client import ClientData
from fido2.ctap2 import AttestedCredentialData, AttestationObject, AuthenticatorData
from fido2.server import Fido2Server
from fido2.utils import websafe_decode, websafe_encode
from fido2.webauthn import PublicKeyCredentialRpEntity
from flask import request, session, Blueprint, abort
from flask_login import login_user

import app.repository.user_credential_repository as user_credential_repository
import app.repository.user_repository as user_repository
from app.database import transaction
from app.model.user_credential import UserCredential

logger = logging.getLogger(__name__)

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')

rp = PublicKeyCredentialRpEntity("localhost", "Demo server")
server = Fido2Server(rp, attestation='direct')


@auth_blueprint.route("/register/begin", methods=["POST"])
@transaction()
def register_begin():
    request_data = request.get_json()
    user = user_repository.find_by_name(request_data['username'])

    # For demo purposes we create the user if does not exist,
    # in a production environment maybe you want to do some validations before adding a user.
    if not user:
        user = user_repository.add_user(request_data['username'])

    logger.info('Begin FIDO2 registration for: ' + user.name)

    credentials = _decode_credentials(user.credentials)
    registration_data, state = server.register_begin(
        {
            "id": str(user.id).encode(),
            "name": user.name,
            "displayName": user.name
        },
        credentials,
        user_verification="discouraged",
        authenticator_attachment="cross-platform",
    )

    session["state"] = state
    return cbor.encode(registration_data)


@auth_blueprint.route("/register/complete", methods=["POST"])
@transaction()
def register_complete():
    data = cbor.decode(request.get_data())
    client_data = ClientData(data["clientDataJSON"])
    att_obj = AttestationObject(data["attestationObject"])
    auth_data = server.register_complete(session["state"], client_data, att_obj)

    encoded_credential_data = websafe_encode(auth_data.credential_data)

    # Store credentials in DB
    user = user_repository.find_by_name(data['username'])
    credential_name = 'MyKey ' + str(len(user.credentials) + 1)
    user_credential_repository.save_credential(user, credential_name, encoded_credential_data)

    logger.info('FIDO2 registration complete for: ' + user.name)
    return cbor.encode({"status": "OK"})


@auth_blueprint.route("/authenticate/begin", methods=["POST"])
def authenticate_begin():
    request_data = request.get_json()
    user_credentials = user_credential_repository.find_by_username(request_data['username'])

    if len(user_credentials) == 0:
        abort(404)

    logger.info('Begin FIDO2 authentication for: ' + request_data['username'])

    credentials = _decode_credentials(user_credentials)
    auth_data, state = server.authenticate_begin(credentials)
    session["state"] = state
    return cbor.encode(auth_data)


@auth_blueprint.route("/authenticate/complete", methods=["POST"])
def authenticate_complete():
    data = cbor.decode(request.get_data())
    user = user_repository.find_by_name(data['username'])

    if len(user.credentials) == 0:
        abort(404)

    credentials = _decode_credentials(user.credentials)
    credential_id = data["credentialId"]
    client_data = ClientData(data["clientDataJSON"])
    auth_data = AuthenticatorData(data["authenticatorData"])
    signature = data["signature"]

    server.authenticate_complete(
        session.pop("state"),
        credentials,
        credential_id,
        client_data,
        auth_data,
        signature,
    )

    login_user(user)

    logger.info('FIDO2 authentication complete for: ' + user.name)
    return cbor.encode({"status": "OK"})


def _decode_credentials(user_credentials: [UserCredential]) -> [AttestedCredentialData]:
    """
    User credentials are stored in base64 and need to be decoded as AttestedCredentialData

    :param user_credentials: User credentials stored in DB.
    :return: Decoded user credentials
    """
    credentials: [AttestedCredentialData] = []
    for user_credential in user_credentials:
        credentials.append(AttestedCredentialData(websafe_decode(user_credential.base64)))

    return credentials
