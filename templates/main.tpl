{% args utils %}
{% include "header.tpl" %}
<h1>Выбор действия</h1>
<div class="row row-cols-1 row-cols-md-3">
    <div class="col mb-4">
        <div class="card text-center border-dark shadow">
            <div class="card-header">Режим рисования</div>
            <div class="card-body">
                <p class="card-text">Можно задать произвольный цвет для каждой лампочки</p>
                <button type="button" class="btn btn-success" data-toggle="modal"
                    data-target=".bd-modal-xl">Начать</button>
            </div>
        </div>
    </div>
    <div class="col mb-4">
        <div class="card text-center border-dark shadow">
            <div class="card-header">Режим эффектов</div>
            <div class="card-body">
                <p class="card-text">Можно настроить и запустить один из эффектов</p>
                <a class="btn btn-success" href="/effects" role="button">Выбрать</a>
            </div>
        </div>
    </div>
    <div class="col mb-4">
        <div class="card text-center border-dark shadow">
            <div class="card-header">Режим шумов</div>
            <div class="card-body">
                <p class="card-text">Можно настроить и запустить один из эффектов</p>
                <a class="btn btn-success" href="/noises" role="button">Выбрать</a>
            </div>
        </div>
    </div>
</div>
{% include "drawing.tpl" utils['1'] %}
{% include "scripts.tpl" %}
<script type="text/javascript">
    $(document).on('change', '.rgb', function () {
        let r = $("#red").val();
        let g = $("#green").val();
        let b = $("#blue").val();
        $("#colorRGB").attr("style", "height: 3rem; border-radius: 1rem; background: rgb(" + r + ", " + g + ", " + b + ");");
    });
    $("td#drawing").click(function () {
        let r = $("#red").val();
        let g = $("#green").val();
        let b = $("#blue").val();
        let info = {
            'id': $(this).attr("value"),
            'r': r, 'g': g, 'b': b
        }
        $.post('set_pixel', info, function (data) {
            console.log(data);
        });
        $(this).attr("style", "background: rgb(" + r + ", " + g + ", " + b + ");");
    });
    $("#clear").click(function () {
        $.post('set_pixel', { 'id': '_' }, function (data) {
            console.log(data);
        });
        $("td#drawing").each(function () {
            $(this).attr("style", "");
        });
    });
</script>
</body>

</html>