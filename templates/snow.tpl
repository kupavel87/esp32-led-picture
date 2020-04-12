{% args prop, id %}
<div class="card">
    <div class="card-header" id="head{{ prop['alias'] }}">
        <h2 class="mb-0">
            <button class="btn btn-link collapsed" type="button" data-toggle="collapse"
                data-target="#collapse{{ prop['alias'] }}" aria-expanded="false"
                aria-controls="collapse{{ prop['alias'] }}">
                {{ prop['name'] }}
            </button>
        </h2>
    </div>
    <div id="collapse{{ prop['alias'] }}" class="collapse" aria-labelledby="head{{ prop['alias'] }}"
        data-parent="#accordion">
        <div class="card-body">
            <button class="btn btn-success" id="start" value={{ id }}>Старт</button>
        </div>
        <div class="card-body">
            <form id="property">
                <div class="row">
                    <div class="col">
                        <label for="customRange1">Скорость</label>
                        <input type="range" class="custom-range" min="1" max="20" step="1" id="customRange1"
                            name="speed" value={{ prop['property']['speed'] }}>
                    </div>
                    <div class="col">
                        <label for="customRange2">Плотность</label>
                        <input type="range" class="custom-range" min="1" max="10" step="1" id="customRange2"
                            name="scale" value={{ prop['property']['scale'] }}>
                    </div>
                    <div class="col">
                        <label for="customRange3">Размытие</label>
                        <input type="range" class="custom-range" min="0" max="100" step="1" id="customRange3"
                            name="pcnt" value={{ prop['property']['pcnt'] }}>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <label for="customRange4">Оттенок</label>
                        <input type="range" class="custom-range hsl" min="0" max="359" step="1" id="hue" name="h"
                            value={{ prop['property']['hsl'][0] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Насыщенность</label>
                        <input type="range" class="custom-range hsl" min="0" max="100" step="1" id="saturation" name="s"
                            value={{ prop['property']['hsl'][1] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Яркость</label>
                        <input type="range" class="custom-range hsl" min="0" max="100" step="1" id="lightness" name="l"
                            value={{ prop['property']['hsl'][2] }}>
                    </div>
                    <div class="col">
                        <div style="height: 3rem; border-radius: 1rem; background: hsl({{prop['property']['hsl'][0]}}, {{prop['property']['hsl'][1]}}%, {{prop['property']['hsl'][2]}}%);"
                            id="result"></div>
                    </div>
                </div>
                <div class="row">
                    <input type="hidden" name="id" value={{ id }}>
                    <div class="col">
                        <button type="submit" class="btn btn-success mt-2">Изменить</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>