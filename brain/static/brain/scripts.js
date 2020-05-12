var resArea = $('#resultsArea');
var modTitle = $('#choiceModal #choiceModalTitle');
var modBody = $('#choiceModal .modal-body #inputActor');
var mod = $('#choiceModal');

function shortest_path(act1, act2) {
  mod.modal('hide');
  
  resArea.empty();
  resArea.append(`<h3 class="text-secondary text-center" >AI is thinking..</h3>`);

  console.log(act1, act2)
  
  $.ajax({
    url: 'ajax/find_path',
    data: {
      'actor1': act1,
      'actor2': act2
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
};

function updateID () {
    var id = $('#inputActor option:selected').val();
    return id;
    
};
function createPrompt (actor, data) {
    modTitle.text(`Which ${actor}?`);
    modBody.empty()
    var i;
    for (i = 0; i < data.length; i++) {
      modBody.append(`
        <option value="${data[i][1]}">${data[i][0]}</option>
      `)
    };

    mod.modal({
      backdrop: 'static'
    });
};

$("#path_button").click(function () {
      
    var input1 = $('#actor1');
    var input2 = $('#actor2');
    
    var actor1= input1.val().toLowerCase();
    var actor2= input2.val().toLowerCase();

    
    


    input1.removeClass('is-invalid')
    input2.removeClass('is-invalid')

    // console.log(actor1);
    // console.log(actor2);
    $.ajax({
      url: 'ajax/validate_name',
      data: {
        'actor1': actor1,
        'actor2': actor2
      },
      dataType: 'json',
      success: function (data) {
        let id1 = data['id1'];
        let id2 = data['id2'];
        
        
        var choices = data['choices'];
        // console.log(choices);
        

        if (data.actor1_isValid && data.actor2_isValid) {
          $('#path_button').prop('disabled', true);
          


          if (!jQuery.isEmptyObject(choices)) {
            
            

            if (typeof choices[actor1] !== 'undefined') {
              createPrompt(actor1, choices[actor1])

              $('#actorChoice').click(function () {
                id1 = updateID()

                if (typeof choices[actor2] !== 'undefined') {
                  createPrompt(actor2, choices[actor2])

                $('#actorChoice').click(function () {
                  console.log('second')
                  id2 = updateID()

                  shortest_path(id1, id2)

                });
                }
                else {
                  shortest_path(id1, id2)
                }
                // console.log(id1)
              });

              if (typeof choices[actor2] !== 'undefined') {
                createPrompt(actor2, choices[actor2])
  
                $('#actorChoice').click(function () {
                  id2 = updateID()
  
                  if (typeof choices[actor1] !== 'undefined') {
                    createPrompt(actor1, choices[actor1])
  
                  $('#actorChoice').click(function () {
                    console.log('second')
                    id1 = updateID()
  
                    shortest_path(id1, id2)
  
                  });
                  }
                  else {
                    shortest_path(id1, id2)
                  }
                  // console.log(id1)
                });

              // modTitle.text(`Which ${actor1}?`);

              // var i;
              // for (i = 0; i < choices[actor1].length; i++) {
              //   // modBody.append(`<p> ${choices[actor1][i]} </p>`);
              //   modBody.append(`
              //     <option value="${choices[actor1][i][1]}">${choices[actor1][i][0]}</option>
              //   `)
              // };

              // mod.modal({
              //   backdrop: 'static'
              // });

              // $('#actorChoice').click(function () {

              //   console.log($('#inputActor option:selected').val());
              //   id1 = $('#inputActor option:selected').val();

              // });
              // console.log('here')
              // id1 = updateID(actor1, choices[actor1]);
              
              // console.log('done')

            };

            // if (typeof choices[actor2] !== 'undefined') {
            //   modTitle.text(`Which ${actor2}?`);

            //   var i;
            //   for (i = 0; i < choices[actor2].length; i++) {
            //     // modBody.append(`<p> ${choices[actor2][i]} </p>`);
            //     modBody.append(`
            //       <option value="${choices[actor2][i][1]}">${choices[actor2][i][0]}</option>
            //     `)
            //   };

            //   mod.modal({
            //     backdrop: 'static'
            //   });

            //   $('#actorChoice').click(function () {
            //     console.log($('#inputActor option:selected').val());
            //     id2 = $('#inputActor option:selected').val();

            //   });
            // };

            
            // console.log(id2);
          }
          else {
            shortest_path(id1, id2)
          }
          
          // console.log(id1);
          // shortest_path(id1, id2);

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

    }
    });
  });
