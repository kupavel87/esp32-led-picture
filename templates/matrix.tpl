{% args prop, id %}
<div class="card">
    <div class="card-header" id="head{{ prop['alias'] }}">
        <h2 class="mb-0">
            <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#collapse{{ prop['alias'] }}"
                aria-expanded="false" aria-controls="collapse{{ prop['alias'] }}">
                {{ prop['name']}}
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
                        <label for="customRange1">Скорость</label>
                        <input type="range" class="custom-range" min="1" max="20" step="1" id="customRange1"
                            name="speed" value={{ prop['property']['speed'] }}>
                    </div>
                    <div class="col">
                        <label for="customRange2">Плотность</label>
                        <input type="range" class="custom-range" min="1" max="10" step="1" id="customRange2"
                            name="scale" value={{ prop['property']['scale'] }}>
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