# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* vincentvanbot/*.py

black:
	@black scripts/* vincentvanbot/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__ */*/__pycache__
	@rm -fr build dist
	@rm -fr vincentvanbot-*.dist-info
	@rm -fr vincentvanbot.egg-info

install:
	@pip install . -U

all: clean install test black check_code


uninstal:
	@python setup.py install --record files.txt
	@cat files.txt | xargs rm -rf
	@rm -f files.txt

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)


# ----------------------------------
#            GOOGLE CLOUD
# ----------------------------------
# initial setup
PROJECT_ID=vincent-van-bot

BUCKET_NAME=vincent-van-bot-bucket

REGION=europe-west1

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}


# upload data
LOCAL_PATH_IMAGES="raw_data/images"
LOCAL_PATH_PICKLE="raw_data/flat_resized_images.pkl"
BUCKET_FOLDER=data
BUCKET_FILE_NAME_IMAGES=$(shell basename ${LOCAL_PATH_IMAGES})
BUCKET_FILE_NAME_PICKLE=$(shell basename ${LOCAL_PATH_PICKLE})

upload_images:
	@gsutil -m cp -r ${LOCAL_PATH_IMAGES} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME_IMAGES}

upload_pickle:
	@gsutil cp ${LOCAL_PATH_PICKLE} gs://${BUCKET_NAME}/${BUCKET_FOLDER}/${BUCKET_FILE_NAME_PICKLE}
