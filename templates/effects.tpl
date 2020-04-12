{% args prop %}
{% include "header.tpl" %}
<h1>Выбор эффекта</h1>
<div class="row row-cols-1 row-cols-md-3">
    {% for id  in prop %}
    <div class="col mb-4">
        <div class="card text-center border-dark shadow">
            <div class="card-header">
                {{ prop[id]['name'] }}
                <span class="badge bg-transparent float-right" id="settings" value={{ id }}>
                    <svg class="bi bi-gear" width="1.5em" height="1.5em" viewBox="0 0 16 16" fill="currentColor"
                        xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd"
                            d="M8.837 1.626c-.246-.835-1.428-.835-1.674 0l-.094.319A1.873 1.873 0 014.377 3.06l-.292-.16c-.764-.415-1.6.42-1.184 1.185l.159.292a1.873 1.873 0 01-1.115 2.692l-.319.094c-.835.246-.835 1.428 0 1.674l.319.094a1.873 1.873 0 011.115 2.693l-.16.291c-.415.764.42 1.6 1.185 1.184l.292-.159a1.873 1.873 0 012.692 1.116l.094.318c.246.835 1.428.835 1.674 0l.094-.319a1.873 1.873 0 012.693-1.115l.291.16c.764.415 1.6-.42 1.184-1.185l-.159-.291a1.873 1.873 0 011.116-2.693l.318-.094c.835-.246.835-1.428 0-1.674l-.319-.094a1.873 1.873 0 01-1.115-2.692l.16-.292c.415-.764-.42-1.6-1.185-1.184l-.291.159A1.873 1.873 0 018.93 1.945l-.094-.319zm-2.633-.283c.527-1.79 3.065-1.79 3.592 0l.094.319a.873.873 0 001.255.52l.292-.16c1.64-.892 3.434.901 2.54 2.541l-.159.292a.873.873 0 00.52 1.255l.319.094c1.79.527 1.79 3.065 0 3.592l-.319.094a.873.873 0 00-.52 1.255l.16.292c.893 1.64-.902 3.434-2.541 2.54l-.292-.159a.873.873 0 00-1.255.52l-.094.319c-.527 1.79-3.065 1.79-3.592 0l-.094-.319a.873.873 0 00-1.255-.52l-.292.16c-1.64.893-3.433-.902-2.54-2.541l.159-.292a.873.873 0 00-.52-1.255l-.319-.094c-1.79-.527-1.79-3.065 0-3.592l.319-.094a.873.873 0 00.52-1.255l-.16-.292c-.892-1.64.902-3.433 2.541-2.54l.292.159a.873.873 0 001.255-.52l.094-.319z"
                            clip-rule="evenodd"></path>
                        <path fill-rule="evenodd"
                            d="M8 5.754a2.246 2.246 0 100 4.492 2.246 2.246 0 000-4.492zM4.754 8a3.246 3.246 0 116.492 0 3.246 3.246 0 01-6.492 0z"
                            clip-rule="evenodd"></path>
                    </svg>
                </span>
            </div>
            <div class="card-body">
                <p class="card-text">{{ prop[id]['description'] }}</p>
            </div>
            <div class="card-footer">
                <button class="btn btn-success" id="start" value={{ id }}>Запустить</button>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
<div class="text-center my-3">
    <button class="btn btn-warning" id="start" value=0>Остановить</button>
</div>
{% include "scripts.tpl" %}
<script type="text/javascript">
    $(document).on('click', '#start', function () {
        $.post('start', { id: $(this).attr("value") }, function (data) {
            console.log(data);
        });
    });
    $(document).on('submit', '#property', function (e) {
        e.preventDefault();

        $.post('set_property', $(this).serialize(), function (data) {
            console.log(data);
        });
    });
    $(document).on('change', '.hsl', function () {
        let h = $("#hue").val();
        let s = $("#saturation").val();
        let l = $("#lightness").val();
        $("#result").attr("style", "height: 3rem; border: 2px solid black; border-radius: 1rem; background: hsl(" + h + ", " + s + "%, " + l + "%);");
        let hsv2hsl = (h, s, v, l = v - v * s / 2, m = Math.min(l, 1 - l)) => [h, m ? (v - l) / m : 0, l];
    });
    $(document).on('input', '.rgb', function () {
        $(this).attr('data-original-title', $(this).val()).tooltip('show');
    });
    $(document).on('change', '.rgb', function () {

        result = '.' + $(this).attr('for');
        let r = $(result + "#red").val();
        let g = $(result + "#green").val();
        let b = $(result + "#blue").val();
        $(result + "Color").attr("style", "height: 3rem; border: 2px solid black; border-radius: 1rem; background: rgb(" + r + ", " + g + ", " + b + ");");
    });
</script>
</body>

</html>