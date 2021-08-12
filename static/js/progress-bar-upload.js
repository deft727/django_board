$(function () {

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    sequentialUploads: true,

    start: function (e) {
      $("#modal-progress").modal("show");
    },

    stop: function (e) {
      $("#modal-progress").modal("hide");
    },

    progressall: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      $(".progress-bar").css({"width": strProgress});
      $(".progress-bar").text(strProgress);
    },

    done: function (e, data) {
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
          `<tr>
            <td> 

              <img src="${data.result.url}"  style="with:35px" /> 
                <a href="" class="my-selector" >${data.result.name}
          <button type="submit" class="close my-selector" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                        </a>
            </td>
          </tr>`
        )
      }
    }
  });
});


$(function(){
  $('.my-selector').click(function(){
    $(this).addClass('js-hidden');
    $(this).removeClass('js-hidden');
    $(this).toggleClass('js-hidden');
  });
});