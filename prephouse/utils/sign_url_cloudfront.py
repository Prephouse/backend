import os
from datetime import date, datetime, timedelta

from botocore.signers import CloudFrontSigner
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def rsa_signer(message):
    cloudfront_pem_file_path = os.environ["CLOUDFRONT_PEM_KEY"]
    with open(cloudfront_pem_file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA256())


def generate_signed_url(distribution_url, manifest_file):
    cloudfront_keyid = os.environ["CLOUDFRONT_KEYID"]
    url = f"{distribution_url}/{manifest_file}"
    today = date.today() + timedelta(days=5)
    expire_date = datetime(
        year=today.year,
        month=today.month,
        day=today.day,
    )
    cloudfront_signer = CloudFrontSigner(cloudfront_keyid, rsa_signer)

    # Create a signed url that will be valid until the specific expiry date
    # provided using a canned policy.
    return cloudfront_signer.generate_presigned_url(url, date_less_than=expire_date)
