#!/usr/bin/zsh

#########################
# GUNICORN CONF EXAMPLE #
#########################

# Votre dossier d'installation
INSTALATION_DIR='/src/keyexchange'
USER=smalakey
GROUP=smalakey
VIRTUALENV_PATH='/vrtlv/exchange_env'



NAME="KeyExchange"
DJANGODIR=$INSTALATION_DIR
SOCKFILE=$INSTALATION_DIR/run/gunicorn.sock
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=KeyExchange.settings
DJANGO_WSGI_MODULE=KeyExchange.wsgi

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
source $VIRTUALENV_PATH/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec $VIRTUALENV_PATH/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
