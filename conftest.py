import logging

from pytest import fixture
from playwright.sync_api import Playwright, sync_playwright
from Page_objects.application import App
import settings


@fixture(autouse=True, scope='session')
def preconditions():
    logging.info('preconditions started')
    yield
    logging.info('postconditions started')

@fixture(scope='session')
def get_playwright():
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def get_browser(get_playwright, request):
    with sync_playwright() as playwright:
        yield playwright


@fixture(scope='session')
def desktop_app(get_playwright):
    app = App(get_playwright, base_url=settings.BASE_URL)
    app.goto('/')
    yield app
    app.close()


@fixture(scope='session')
def desktop_app_auth(desktop_app):
    app = desktop_app
    app.goto('/login')
    app.login(**settings.USER)
    yield app




