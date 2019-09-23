from redis import Redis

from swiper_social.cfg import REDIS

rds = Redis(**REDIS)