# from cassandra.cluster import Cluster
# from cassandra.auth import PlainTextAuthProvider
from langchain_community.chat_message_histories import CassandraChatMessageHistory
from langchain.memory import ConversationBufferMemory
import json

def setup_memory():
    cloud_config = {
        'secure_connect_bundle': 'secure-connect-charlas.zip'
    }
    
    with open("tharasoft.origen@gmail.com-token.json") as f:
        secrets = json.load(f)
    
    CLIENT_ID = secrets["clientId"]
    CLIENT_SECRET = secrets["secret"]
    ASTRA_DB_KEYSPACE = "charlas"
    
    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    
    message_history = CassandraChatMessageHistory(
        session_id="anything",
        session=session,
        keyspace=ASTRA_DB_KEYSPACE,
        ttl_seconds=3600
    )
    
    message_history.clear()
    
    cass_buff_memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=message_history
    )
    
    return cass_buff_memory