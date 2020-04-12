{% args prop, id %}
<div class="card">
    <div class="card-header" id="head{{ prop['alias'] }}">
        <h2 class="mb-0">
            <button class="btn btn-link collapsed" type="button" data-toggle="collapse" data-target="#collapse{{ prop['alias'] }}"
                aria-expanded="false" aria-controls="collapse{{ prop['alias'] }}">
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
                        <div class="form-group row">
                            <label for="exampleFormControlSelect1" class="col-2 col-form-label">Метод</label>
                            <div class="col-10">
                                <select class="form-control" id="exampleFormControlSelect1" name="select">
                                    <option value="1" {% if prop['property']['type'] == 1 %}selected{% endif %}>Радуга</option>
                                    <option value="0" {% if prop['property']['type'] == 0 %}selected{% endif %}>Спектр</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <input type="hidden" name="id" value={{ id }}>
                    <div class="col">
                        <button type="submit" class="btn btn-success">Изменить</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>