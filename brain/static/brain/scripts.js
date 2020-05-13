var resArea = $('#resultsArea');
var modTitle = $('#choiceModal #choiceModalTitle');
var modBody = $('#choiceModal .modal-body #inputActor');
var modFooter = $('#choiceModal .modal-footer');
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

      // display results
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
      // enable the button again
      $('#path_button').prop('disabled', false);
    }
  });
};

function updateID () {
    var id = $('#inputActor option:selected').val();
    return id;
    
};
function createPrompt (actor, data, identity) {
    modBody.empty();
    modFooter.empty();
    modTitle.text(`Which ${actor}?`);
    // button has to recreated since we don't want the click event listener for previous modal dialog to also be fired 
    modFooter.append(`
      <button type="button" id="${identity}" class="btn btn-dark">Confirm</button>
    `)
    
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

    console.log(actor1);
    console.log(actor2);

    $.ajax({
      url: 'ajax/validate_name',
      data: {
        'actor1': actor1,
        'actor2': actor2
      },
      dataType: 'json',
      success: function (data) {
        console.log(data)
        let id1 = data['id1'];
        let id2 = data['id2'];
        
        var choices = data['choices'];
        // make sure both names are valid
        if (data.actor1_isValid && data.actor2_isValid) {
          // disable the button until the path has been found to avoid multiple clicks
          $('#path_button').prop('disabled', true);
          // check if multiple actor logs exist for the same name
          if (!jQuery.isEmptyObject(choices)) {

            // clarify the identity of the actor
            if (typeof choices[actor1] !== 'undefined') {
              createPrompt(actor1, choices[actor1], 'actor1Choice');

              $('#actor1Choice').click(function () {
                id1 = updateID()

                if (typeof choices[actor2] !== 'undefined') {
                  createPrompt(actor2, choices[actor2], 'actor2Choice');

                  $('#actor2Choice').click(function () {
                    console.log('second')
                    id2 = updateID()

                    shortest_path(id1, id2);
                  });
                }
                else {
                  shortest_path(id1, id2);
                }
              });
            }
            else if (typeof choices[actor2] !== 'undefined') {
              createPrompt(actor2, choices[actor2], 'actor2Choice');

              $('#actor2Choice').click(function () {
                id2 = updateID();

                if (typeof choices[actor1] !== 'undefined') {
                  createPrompt(actor1, choices[actor1], 'actor1Choice');

                  $('#actor1Choice').click(function () {
                    console.log('second')
                    id1 = updateID()

                    shortest_path(id1, id2);
                  });
                }
                else {
                  shortest_path(id1, id2);
                }
              });
            }

          }
          // otherwise proceed to get the path
          else {
            shortest_path(id1, id2);
          };
        
        }

        else {
            // show user which actor name is invalid
            if (!data.actor1_isValid) {
              input1.addClass('is-invalid');
            }
            if (!data.actor2_isValid) {
              input2.addClass('is-invalid');
            }
        }
      }

    });
  });
