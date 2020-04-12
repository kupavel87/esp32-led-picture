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
                        <label>Цвет передних фар</label>
                    </div>
                    <div class="col">
                        <label for="customRange4">Красный</label>
                        <input type="range" class="custom-range rgb front" for="front" min="0" max="255" step="1"
                            id="red" value={{ prop['property']['frontColor'][0] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Зеленый</label>
                        <input type="range" class="custom-range rgb front" for="front" min="0" max="255" step="1"
                            id="green" value={{ prop['property']['frontColor'][1] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Синий</label>
                        <input type="range" class="custom-range rgb front" for="front" min="0" max="255" step="1"
                            id="blue" value={{ prop['property']['frontColor'][2] }}>
                    </div>
                    <div class="col">
                        <div style="height: 3rem; border-radius: 1rem; background: rgb({{ prop['property']['frontColor'][0] }}, {{ prop['property']['frontColor'][1] }}, {{ prop['property']['frontColor'][2] }});"
                            class="frontColor"></div>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <label>Цвет задних фар</label>
                    </div>
                    <div class="col">
                        <label for="customRange4">Красный</label>
                        <input type="range" class="custom-range rgb rear" for="rear" min="0" max="255" step="1" id="red"
                            value={{ prop['property']['rearColor'][0] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Зеленый</label>
                        <input type="range" class="custom-range rgb rear" for="rear" min="0" max="255" step="1"
                            id="green" value={{ prop['property']['rearColor'][1] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Синий</label>
                        <input type="range" class="custom-range rgb rear" for="rear" min="0" max="255" step="1"
                            id="blue" value={{ prop['property']['rearColor'][2] }}>
                    </div>
                    <div class="col">
                        <div style="height: 3rem; border-radius: 1rem; background: rgb({{ prop['property']['rearColor'][0] }}, {{ prop['property']['rearColor'][1] }}, {{ prop['property']['rearColor'][2] }});"
                            class="rearColor"></div>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <label>Цвет машин</label>
                    </div>
                    <div class="col">
                        <label for="customRange4">Красный</label>
                        <input type="range" class="custom-range rgb car" for="car" min="0" max="255" step="1" id="red"
                            value={{ prop['property']['carColor'][0] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Зеленый</label>
                        <input type="range" class="custom-range rgb car" for="car" min="0" max="255" step="1" id="green"
                            value={{ prop['property']['carColor'][1] }}>
                    </div>
                    <div class="col">
                        <label for="customRange4">Синий</label>
                        <input type="range" class="custom-range rgb car" for="car" min="0" max="255" step="1" id="blue"
                            value={{ prop['property']['carColor'][2] }}>
                    </div>
                    <div class="col">
                        <div style="height: 3rem; border-radius: 1rem; background: rgb({{ prop['property']['carColor'][0] }}, {{ prop['property']['carColor'][1] }}, {{ prop['property']['carColor'][2] }});"
                            class="carColor"></div>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <label for="customRange1">Скорость</label>
                        <input type="range" class="custom-range" min="1" max="20" step="1" id="customRange1"
                            name="speed" value={{prop['property']["speed"]}}>
                    </div>
                    <div class="col">
                        <label for="customRange2">Размер</label>
                        <input type="range" class="custom-range" min="3" max="6" step="1" id="customRange2" name="size"
                            value={{prop['property']["size"]}}>
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