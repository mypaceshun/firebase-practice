# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn, firestore_fn
from firebase_admin import initialize_app, firestore
import google.cloud.firestore

app = initialize_app()


@https_fn.on_request()
def add_message(request: https_fn.Request) -> https_fn.Response:
    original = request.args.get("text")
    if original is None:
        return https_fn.Response("No text provided", status=400)
    firestore_client: google.cloud.firestore.Client = firestore.client()
    _, doc_ref = firestore_client.collection("messages").add({"original": original})
    return https_fn.Response(f"Document written with ID: {doc_ref.id}")


@firestore_fn.on_document_created(document="messages/{pushId}")
def makeuppercase(
    event: firestore_fn.Event[firestore_fn.DocumentSnapshot | None],
) -> None:
    if event.data is None:
        return
    try:
        original = event.data.get("original")
    except ValueError:
        return
    print(f"Uppercasing {event.params['pushId']}: {original}")
    upper = original.upper()
    event.data.reference.update({"uppercase": upper})
