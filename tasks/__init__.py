from invoke import run, task


@task
def flake8(c):
    run("flake8 .")


@task
def isort_check(c):
    run("isort --check -rc .")


@task
def black_check(c):
    run("black --check .")


@task
def isort(c):
    run("isort .")


@task
def black(c):
    run("black .")


@task
def pytest(c):
    run("pytest .")


@task(pre=[flake8, isort_check, black_check])
def lint(c):
    pass


@task(pre=[isort, black])
def fix(c):
    pass


@task(pre=[pytest])
def test(c):
    pass
