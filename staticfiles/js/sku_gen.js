<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

document.addEventListener('DOMContentLoaded', function() {
  function generateSKU() {
    var randomSKU = Math.floor(Math.random() * 9000) + 1000 + '-' +
                    Math.floor(Math.random() * 1000) + '-' +
                    Math.floor(Math.random() * 10000);
    return randomSKU;
  }

  function updateSKUField() {
    var skuGenRadio = document.querySelector('input[name="sku_gen"]:checked');
    var skuField = document.getElementById('id_sku');
    var generatedSKUElement = document.getElementById('generated-sku');
    if (skuGenRadio && skuGenRadio.value === 'auto') {
      var generatedSKU = generateSKU();
      skuField.value = generatedSKU;
      generatedSKUElement.textContent = 'Generated SKU: ' + generatedSKU;
    } else {
      skuField.value = '';
      generatedSKUElement.textContent = '';
    }
  }

  var skuGenRadios = document.querySelectorAll('input[name="sku_gen"]');
  skuGenRadios.forEach(function(radio) {
    radio.addEventListener('change', updateSKUField);
  });

  updateSKUField();
});
