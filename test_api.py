import logging
import requests
from time import sleep

from agent.rtm.client import AgentRTMInterface
from configuration.client import ConfigurationApiInterface
from customer.rtm.client import CustomerRTMInterface


def test_agent_login_unsuccessful(agent_rtm):
    assert agent_rtm.login(
    )['response']['payload']['error']['message'] == "Invalid access token"


def test_agent_login(agent_rtm, pytestconfig):
    assert agent_rtm.login(
        token=pytestconfig.getoption('--agent'))['response']['success'] == True



def test_webhook_(configuration_api: ConfigurationApiInterface,
                  agent_rtm: AgentRTMInterface,
                  customer_rtm: CustomerRTMInterface, pytestconfig):
    '''
        This test registers 'chat_properties_updated' webhook,
        Starts new chat as the customer and asserts the webhook is received to an URL
        specified during the webhook registration.
    '''

    # This should actually go to setup fixture
    configuration_api.register_webhook(
            action='chat_properties_updated',
            secret_key='InbaTrwa420',
            url='https://webhook.site/7b9c6f4b-b829-4542-8334-4e790a1c6a67',
            owner_client_id=pytestconfig.getoption('--client_id'),type='license').json(),
    configuration_api.enable_license_webhooks(owner_client_id=pytestconfig.getoption('--client_id')).json()

    agent_rtm.login(token=pytestconfig.getoption('--agent'))
    customer_rtm.login(token=pytestconfig.getoption('--customer'))
    customer_rtm.start_chat()
    customer_rtm.ws.close()
    agent_rtm.ws.close()
    # let's assume there's a slight delay for delivering the webhook
    sleep(2)
    received_requests = requests.get(
        'https://webhook.site/token/7b9c6f4b-b829-4542-8334-4e790a1c6a67/requests'
    ).json()
    logging.info(received_requests)
    # This assumes 'data' list from the response is not empty
    assert received_requests['data']
