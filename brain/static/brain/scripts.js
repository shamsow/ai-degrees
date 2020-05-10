$("#path_button").click(function () {
      
    var input1 = $('#actor1');
    var input2 = $('#actor2');
    
    var actor1= input1.val();
    var actor2= input2.val();

    var resArea = $('#resultsArea');
    


    input1.removeClass('is-invalid')
    input2.removeClass('is-invalid')

    console.log(actor1);
    console.log(actor2)
    $.ajax({
      url: 'ajax/validate_name',
      data: {
        'actor1': actor1,
        'actor2': actor2
      },
      dataType: 'json',
      success: function (data) {
        
        if (data.actor1_isValid && data.actor2_isValid) {
          resArea.empty()
          resArea.append(`<h3 class="text-secondary text-center" >AI is thinking..</h3>`)
          

          $('#path_button').prop('disabled', true);

          $.ajax({
            url: 'ajax/find_path',
            data: {
              'actor1': actor1,
              'actor2': actor2
            },
            dataType: 'json',
            success: function (data) {
              resArea.empty()

              let path = data['path']
              let degrees = data['degrees']
              
              console.log(path)

              resArea.append(`<h3 class="text-secondary text-center mb-2" >${degrees} Degrees of Separation</h3>`)
              var j;
              var points = '';
              for (j = 0; j < degrees; j++) {
                  points = points.concat('<li></li>')
              };

              resArea.append(`<ul class="m-4" id="degrees_line">${points}</ul>`)

              // degreesLine.css("display", "block")

              var i;
              for (i = 0; i < degrees; i++) {
                
                resArea.append(`
                <div class="card m-3 mx-auto w-100">
                  <div class="card-body">
                    <h3 class="card-title">${path[i]['movie']}</h3>
                    <p class="card-subtitle mb-2 text-muted">${path[i]['names']}</p>
                    <h4 class="card-text text-info">${path[i]['description']}</h4>
                  </div>
                </div>
                `);
              };
              $('#path_button').prop('disabled', false);
            }
          });
        }
        else {
            
            if (!data.actor1_isValid) {
              // document.getElementById('actor1').classList.add('is-invalid')
              input1.addClass('is-invalid');
            }
            if (!data.actor2_isValid) {
              // document.getElementById('actor2').classList.add('is-invalid')
              input2.addClass('is-invalid');
            }
        }
      }
    });
  });