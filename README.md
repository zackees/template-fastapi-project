# template-fastapi-project


#### Platform tests

[![Actions Status](../../workflows/MacOS_Tests/badge.svg)](../../actions/workflows/test_macos.yml)
[![Actions Status](../../workflows/Win_Tests/badge.svg)](../../actions/workflows/test_win.yml)
[![Actions Status](../../workflows/Ubuntu_Tests/badge.svg)](../../actions/workflows/test_ubuntu.yml)

#### Lint

[![Actions Status](../../workflows/Lint/badge.svg)](../../actions/workflows/lint.yml)

Example FastAPI Project with Docker, ready for Render.com / DigitalOcean

Simply change the names `template-fastapi-project` and `template_fastapi_project` to `my-app` and `my_app` and then run `tox` to
confirm that the changes are correct.

To deploy the test app simply fork the repository and go to Render.com, login with your github account, and select this repo that you forked in your account. It should run without any changes.
