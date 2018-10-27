import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('tags')


cartoes = {
    '708419173228' : 'julio',
    '424222889189' : 'lucas'
}


for id, usuario in cartoes.items():
    table.put_item(
        Item={
            'id': id,
            'usuario': usuario
        }
    )
    print(id, ': ', usuario)

