from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .serializers import *
from .models import *
import json
from django.core.serializers import serialize
import jwt
from datetime import datetime
import logging
logger = logging.getLogger('django')

def check_validation(token: str) -> bool:
    try:
        # Decode the JWT without verifying the signature
        payload = jwt.decode(token, 'some-large-secret-in-production', algorithms=['HS256'],
                             options={"verify_signature": False})

        # Extract the expiration time from the payload
        expiration_time = datetime.utcfromtimestamp(payload['exp'])

        # Check if the token has expired
        if expiration_time < datetime.utcnow():
            return False
        else:
            return True
    except jwt.ExpiredSignatureError:
        # Token has expired
        return False
    except jwt.InvalidTokenError:
        # Token is invalid
        return False

# view for creating a note
@api_view(["POST"])
def create_note(request):
    try:
        token = request.headers['Authorization']
        if not check_validation(token):
            return Response('Unauthorized Request', status=status.HTTP_401_UNAUTHORIZED)
        serializer = noteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f'Create Note:{e}')
        return Response('Something went wrong at our end', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# view for fetching a note by id
@api_view(["GET"])
def fetch_note(request, id):
    try:
        token = request.headers['Authorization']
        if not check_validation(token):
            return Response('Unauthorized Request', status=status.HTTP_401_UNAUTHORIZED)
        note = Note.object.select_related('owner').get(id=id)
        return Response({"note": note.content, "owner": note.owner.name},
                        status=status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response('Note does not exists', status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'Fetch Notes:{e}')
        return Response('something went wrong at our end', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# view for sharing the note
@api_view(["POST"])
def share_note(request):
    try:
        token = request.headers['Authorization']
        if not check_validation(token):
            return Response('Unauthorized Request', status=status.HTTP_401_UNAUTHORIZED)
        note = Note.object.select_related('owner').get(id=request.data['note'])
        new_content = {
            "owner": note.owner.id,
            "content": note.content,
            "share": note.share,
        }
        user_shared = json.loads(note.share)
        user_shared.append(request.data['user'])
        new_content['share'] = str(user_shared)
        serializer = noteSerializer(instance=note, data=new_content)
        if serializer.is_valid():
            serializer.save()
            return Response('Note shared with user', status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response("User does not exists", status=status.HTTP_404_NOT_FOUND)

    except ObjectDoesNotExist:
        return Response('Note does not exists', status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'Share Note:{e}')
        return Response('something went wrong at our end', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# view for updating the note
@api_view(["PUT"])
def update_note(request, id):
    try:
        token = request.headers['Authorization']
        if not check_validation(token):
            return Response('Unauthorized Request', status=status.HTTP_401_UNAUTHORIZED)
        note = Note.object.select_related('owner').get(id=id)
        # checking is user has permission to edit this note
        shared = json.loads(note.share)
        modifier = request.data['modifier']
        if modifier in shared or note.owner.id == modifier:
            id = note.id
            owner = note.owner.id
            share = note.share
            old_content = note.content
            new_content = request.data['content']
            # update the existing note
            serializer = noteSerializer(instance=note, data={"owner": owner, "content": new_content,
                                                             "share": share})
            if serializer.is_valid():
                serializer.save()
                # update the changes record
                change = {
                    "user": modifier,
                    "note": id,
                    "prev": old_content,
                    "new": new_content,
                }
                change_serializer = changeSerializer(data=change)
                if change_serializer.is_valid():
                    change_serializer.save()
                    return Response({"message": "Note updated and changes recorded",
                                     "note": change_serializer.validated_data},
                                    status=status.HTTP_200_OK)
                else:
                    print(change_serializer.errors)
                    return Response("Note updated successfully", status=status.HTTP_200_OK)

            else:
                return Response("Something went wrong unable to update document",
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("You don't have permission to edit this note", status=status.HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist:
        return Response('Note does not exists', status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'User login:{e}')
        return Response('Update Note', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# view for fetching all the changes made to the note
@api_view(["GET"])
def get_changes(request, id):
    try:
        token = request.headers['Authorization']
        if not check_validation(token):
            return Response('Unauthorized Request', status=status.HTTP_401_UNAUTHORIZED)

        changes = Change.object.filter(note=id)

        if len(changes) != 0:
            serialized_data = serialize('json', changes)
            serialized_data = json.loads(serialized_data)
            formatted_data = [d['fields'] for d in serialized_data]
            print(formatted_data)
            return Response({"message": "Changes made", "data": formatted_data}, status=status.HTTP_200_OK)

        else:
            return Response('No changes made', status=status.HTTP_404_NOT_FOUND)

    except ObjectDoesNotExist:
        return Response('No changes made', status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f'Get version history:{e}')
        return Response('something went wrong at our end', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

