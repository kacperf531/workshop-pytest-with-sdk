

from agent.rtm.client import AgentRTM
from customer.rtm.client import CustomerRTM
from configuration.client import ConfigurationApi
import pytest


@pytest.fixture
def agent_rtm():
    return AgentRTM.get_client()

@pytest.fixture
def customer_rtm(pytestconfig):
    return CustomerRTM.get_client(int(pytestconfig.getoption('--license')))

@pytest.fixture
def configuration_api(pytestconfig):
    return ConfigurationApi.get_api_client(token=pytestconfig.getoption('--agent'))

@pytest.fixture(autouse=True)
def teardown(agent_rtm, customer_rtm):
    yield
    agent_rtm.logout()
    agent_rtm.ws.close()
    customer_rtm.ws.close()

def pytest_addoption(parser):
    parser.addoption('--agent')
    parser.addoption('--customer')
    parser.addoption('--license')
    parser.addoption('--client_id')
