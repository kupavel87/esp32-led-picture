{% args prop, id %}
<div class="card">
    <div class="card-header" id="head{{ prop['alias'] }}">
        <h2 class="mb-0">
            <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#collapse{{ prop['alias'] }}"
                aria-expanded="true" aria-controls="collapse{{ prop['alias'] }}">
                {{ prop['name'] }}
            </button>
        </h2>
    </div>
    <div id="collapse{{ prop['alias'] }}" class="collapse" aria-labelledby="head{{ prop['alias'] }}" data-parent="#accordion">
        <div class="card-body">
            <button class="btn btn-success" id="start" value={{ id }}>Старт</button>
        </div>
        <div class="card-body">
            <form id="property">
                <div class="row">
                    <div class="col">
                        <label>Цвет куба</label>
                    </div>
                    <div class="col">
                        <label for="customRange4">Красный</label>
                        <input type="range" class="custom-range rgb cube" for="cube" min="0" max="255" step="1" id="red" value={{ prop['property']['cubeColor'][0] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Зеленый</label>
                        <input type="range" class="custom-range rgb cube" for="cube" min="0" max="255" step="1" id="green" value={{ prop['property']['cubeColor'][1] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Синий</label>
                        <input type="range" class="custom-range rgb cube" for="cube" min="0" max="255" step="1" id="blue" value={{ prop['property']['cubeColor'][2] }}>
                    </div>
                    <div class="col">
                        <div style="height: 3rem; border-radius: 1rem; background: rgb({{ prop['property']['cubeColor'][0] }}, {{ prop['property']['cubeColor'][1] }}, {{ prop['property']['cubeColor'][2] }});"
                            class="cubeColor"></div>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <label for="customRange1">Скорость</label>
                        <input type="range" class="custom-range" min="1" max="10" step="1" id="customRange1"
                            name="speed" value={{prop['property']['speed']}}>
                    </div>
                    <div class="col">
                        <label for="customRange2">Размер</label>
                        <input type="range" class="custom-range" min="2" max="4" step="1" id="customRange2"
                            name="size" value={{prop['property']['size']}}>
                    </div>
                    <input type="hidden" name="id" value={{ id }}>
                    <div class="col">
                        <button type="submit" class="btn btn-success mt-2">Изменить</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>