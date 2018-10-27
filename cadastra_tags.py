import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('tags')


cartoes = {
    '708419173228' : 'julio',
    '424222889189' : 'lucas'
    '561061060': 'teste'
}


for id, usuario in cartoes.items():
    table.put_item(
        Item={
            'id': id,
            'usuario': usuario
        }
    )
    print(id, ': ', usuario)

