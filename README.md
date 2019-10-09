usage:

    docker run --rm -ti -v `pwd`:/code -w /code photoweb ./run build

    docker run --rm -ti -v `pwd`:/code -w /code photoweb ./run serve

Deps: 

    docker
    ./docker/build.sh

Upload:

    scp -r _build/* root@photo.mofo.ca:/var/www/photo_mofo_ca/.
