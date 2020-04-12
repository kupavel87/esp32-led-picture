import asyn
import picoweb
import logging
import uasyncio as asyncio
import utime

import led_init
import settings

logging.basicConfig(level=logging.INFO)

app = picoweb.WebApp(__name__)
log = logging.getLogger("websrv")
start_property = settings.effects
start_utils = settings.utils
led_status = None


def time2str():
    t = utime.localtime()
    return "{}-{}-{} {}:{}:{}".format(t[2], t[1], t[0], t[3], t[4], t[5])


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp)
    yield from app.render_template(resp, "main.tpl", (start_utils,))


@app.route("/effects")
def index(req, resp):
    yield from picoweb.start_response(resp)
    effects = ('1', '2', '3', '4', '5', '6', '7')
    yield from app.render_template(resp, "effects.tpl", ({k: start_property[k] for k in effects},))


@app.route("/noises")
def index(req, resp):
    yield from picoweb.start_response(resp)
    noises = ('11', '12', '13', '14', '15', '16', '17')
    yield from app.render_template(resp, "noises.tpl", ({k: start_property[k] for k in noises},))


@app.route("/start")
def start(req, resp):
    global led_status
    if req.method == "POST":
        yield from req.read_form_data()
        log.info("{} {} {} {}".format(time2str(), 'Команда:', 'start', req.form))
        id = req.form["id"]
        if id in start_property:
            if led_status or id == "0":
                yield from asyn.NamedTask.cancel(led_status)
                log.info("{} {}".format(time2str(), 'Задача остановлена'))
                led_init.led_off()
                led_status = None
            else:
                led_status = start_property[id]['name']
                loop.create_task(asyn.NamedTask(
                    led_status, start_property[id]['function'], start_property[id]['property'])())
                log.info("{} {} {}".format(time2str(), 'Задача запущена:', led_status))
        else:
            yield from picoweb.start_response(resp, status=404)
            yield from resp.awrite("id {} not found!".format(req.form["id"]))
            return
    yield from picoweb.start_response(resp)
    yield from resp.awrite("id {} done!".format(req.form["id"]))


@app.route("/set_property")
def set_property(req, resp):
    global led_status
    global start_property
    status = 404
    answer = ''
    if req.method == "POST":
        yield from req.read_form_data()
        log.info("{} {} {} {}".format(time2str(), 'Команда:', 'set_property', req.form))
        id = req.form["id"]
        if id in start_property:
            for prop_name in start_property[id]['property']:
                if prop_name == 'hsl':
                    start_property[id]['property']['hsl'] = (int(req.form['h']), int(req.form['s']), int(req.form['l']))
                else:
                    start_property[id]['property'][prop_name] = int(req.form[prop_name])
            if led_status is not None:
                yield from asyn.NamedTask.cancel(led_status)
                led_status = "re{}".format(led_status)
                loop.create_task(asyn.NamedTask(
                    led_status, start_property[id]['function'], start_property[id]['property'])())
                log.info("{} {} {}".format(time2str(), 'Задача запущена:', led_status))
        else:
            answer = "Error! id {} not found!".format(req.form["id"])
        if not answer:
            status = 200
            answer = "id {} done!".format(req.form["id"])
    else:
        answer = "Error! Method not found!"
    yield from picoweb.start_response(resp, status=status)
    yield from resp.awrite(answer)


@app.route("/set_pixel")
def set_pixel(req, resp):
    global led_status
    status = 404
    if req.method == "POST":
        if led_status:
            yield from asyn.NamedTask.cancel(led_status)
            log.info("{} {}".format(time2str(), 'Задача остановлена'))
            led_init.led_off()
            led_status = None
        yield from req.read_form_data()
        log.info("{} {} {} {}".format(time2str(), 'Команда:', 'set_pixel', req.form))
        id_str = req.form['id']
        y, x = id_str.split('_')
        if y:
            color = (int(req.form['r']), int(req.form['g']), int(req.form['b']))
            led_init.setColorXY(int(x), 11 - int(y), color)
            led_init.pixels.write()
            answer = "Done! ({}, {}) = {}".format(x, 11 - int(y), color)
        else:
            led_init.pixels.fill((0, 0, 0))
            led_init.pixels.write()
            answer = "Clear done!"
        status = 200
    else:
        answer = "Error! Method not found!"
    yield from picoweb.start_response(resp, status=status)
    yield from resp.awrite(answer)


@app.route("/reboot")
def reboot(req, resp):
    machine.reset()


start_property['1']['function'] = led_init.move_cube
start_property['2']['function'] = led_init.move_fire
start_property['3']['function'] = led_init.move_rainbow
start_property['4']['function'] = led_init.move_snow
start_property['5']['function'] = led_init.move_matrix
start_property['6']['function'] = led_init.move_cars
start_property['7']['function'] = led_init.move_clouds
start_property['11']['function'] = led_init.lavaNoise
start_property['12']['function'] = led_init.plasmaNoise
start_property['13']['function'] = led_init.cloudNoise
start_property['14']['function'] = led_init.oceanNoise
start_property['15']['function'] = led_init.forestNoise
start_property['16']['function'] = led_init.rainbowNoise
start_property['17']['function'] = led_init.rainbowStripeNoise
led_init.led_off()
loop = asyncio.get_event_loop()
app.log = log
app.debug = 0
app.init()
print("* Start work. Ver.14")
led_init.led.value(1)
app.serve(loop, '0.0.0.0', 80)
print("* End work")
