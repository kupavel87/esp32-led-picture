{% args prop %}
<div class="modal fade bd-modal-xl" tabindex="-1" role="dialog"
    aria-labelledby="myExtraLargeModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl" role="document">
        <div class="modal-content">
            <div class="modal-body">
                <table class="table table-sm table-bordered">
                    <thead>
                    </thead>
                    <tbody>
                        {% for y in range(prop['property']['height']) %}
                        <tr style="height: 2rem;">
                            {% for x in range(prop['property']['width']) %}
                            <td id="drawing" value="{{y}}_{{x}}"> </td>
                            {% endfor %}
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div class="modal-footer">
                <div class="row">
                    <div class="col">
                        <button type="button" class="btn btn-success mt-2" id="clear">Очистить</button>
                    </div>
                    <div class="col">
                        <label for="customRange4">Красный</label>
                        <input type="range" class="custom-range rgb" min="0" max="255" step="1" id="red" value=255>
                    </div>
                    <div class="col">
                        <label for="customRange4">Зеленый</label>
                        <input type="range" class="custom-range rgb" min="0" max="255" step="1" id="green" value=0>
                    </div>
                    <div class="col">
                        <label for="customRange4">Синий</label>
                        <input type="range" class="custom-range rgb" min="0" max="255" step="1" id="blue" value=0>
                    </div>
                    <div class="col">
                        <div style="height: 3rem; border-radius: 1rem; background: rgb(255, 0, 0);"
                            id="colorRGB"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>