$(document).ready(function () {
  
    // Denotes total number of rows
    var rowIdx = 0;

    // jQuery button click event to add a row
    $('#addBtn').on('click', function () {

        let colIdx =0;

      // Adding a row inside the tbody.
      $('#tbody').append(`<tr id="R${++rowIdx}">
          <td class="row-index text-center">
              <input type="text" placeholder="Enter Time" class="form-control " id = "R${rowIdx}${++colIdx}"/>
          </td>
          <td class="row-index text-center">
              <input type="text" placeholder="Enter Activity" class="form-control " id = "R${rowIdx}${++colIdx}"/>
          </td>
          <td class="row-index text-center">
              <input type="text" placeholder="Enter Activity" class="form-control " id = "R${rowIdx}${++colIdx}"/>
          </td>
          <td class="row-index text-center">
              <input type="text" placeholder="Enter Activity" class="form-control " id = "R${rowIdx}${++colIdx}"/>
          </td>
          <td class="row-index text-center">
              <input type="text" placeholder="Enter Activity" class="form-control " id = "R${rowIdx}${++colIdx}"/>
          </td>
          <td class="row-index text-center">
              <input type="text" placeholder="Enter Activity" class="form-control " id = "R${rowIdx}${++colIdx}"/>
          </td>
          <td class="row-index text-center">
              <input type="text" placeholder="Enter Activity" class="form-control " id = "R${rowIdx}${++colIdx}"/>
          </td>
          <td class="text-center">
              <button class="btn btn-outline-danger remove sm"
                type="button">Delete</button>
              </td>
            </tr>`);
    });



    //TO DELETE ROWS

    // jQuery button click event to remove a row.
    $('#tbody').on('click', '.remove', function () {

      // Getting all the rows next to the row
      // containing the clicked button
      var child = $(this).closest('tr').nextAll();

      // Iterating across all the rows 
      // obtained to change the index
      child.each(function () {

          // Getting <tr> id.
          var id = $(this).attr('id');

          // Getting the <p> inside the .row-index class.
          var idx = $(this).children('.row-index').children('p');

          // Gets the row number from <tr> id.
          var dig = parseInt(id.substring(1));

          // Modifying row index.
          idx.html(`Row ${dig - 1}`);

          // Modifying row id.
          $(this).attr('id', `R${dig - 1}`);
      });

      // Removing the current row.
      $(this).closest('tr').remove();

      // Decreasing total number of rows by 1.
      rowIdx--;
      });



      /*//BOLD BUTTON

      $('.boldBtn').on('click', function () {
        // Check if the bold button is toggled on or off
        var isBold = $(this).hasClass('active');
    
        // Get all the input fields with class "activity-input"
        var activityInputs = $('input[id = "R12"]');
    
        // Toggle the font-weight style for the input fields
        activityInputs.css('font-weight', isBold ? 'normal' : 'bold');
    
        // Toggle the "active" class to indicate the button state
        $(this).toggleClass('active', !isBold);
      });



      //ITALIC BUTTON
    
      $('.italicBtn').on('click', function () {
        // Check if the italic button is toggled on or off
        var isItalic = $(this).hasClass('active');
    
        // Get all the input fields with class "activity-input"
        var activityInputs = $('input[id = "R12"]');
    
        // Toggle the font-style style for the input fields
        activityInputs.css('font-style', isItalic ? 'normal' : 'italic');
    
        // Toggle the "active" class to indicate the button state
        $(this).toggleClass('active', !isItalic);
      });



      //UNDERLINE BUTTON

      $('.underlineBtn').on('click', function () {
        // Check if the underline button is toggled on or off
        var isUnderline = $(this).hasClass('active');
    
        // Get all the input fields with class "activity-input"
        var activityInputs = $('input[id = "R12"]');
    
        // Toggle the text-decoration style for the input fields
        activityInputs.css('text-decoration', isUnderline ? 'none' : 'underline');
    
        // Toggle the "active" class to indicate the button state
        $(this).toggleClass('active', !isUnderline);
      });*/

      /*//COLOR BUTTON FOR ALL

      $('.colorBtn').spectrum({
        preferredFormat: "rgb",
        showPalette: true,
        palette: [
          ["#000", "#fff", "#ff0000", "#00ff00", "#0000ff"], // Background color palette
          //["#000", "#fff", "#ff0000", "#00ff00", "#0000ff"], // Text color palette
        ],
        change: function (color) {
          var selectedColor = color.toHexString();
          
          // Set background color and text color for all input fields
          $('input[type="text"]').css({
            "background-color": selectedColor,
            //"color": selectedColor === "#000" ? "#fff" : "#000", // Set text color based on background color
          });
        },
      });*/




    // Event delegation to detect the selected input field
    $('#tbody').on('click', 'input[type="text"]', function () {
        selectedInput = this;
    });

    // BOLD BUTTON
    $('.boldBtn').on('click', function () {
        if (selectedInput) {
            // Check if the bold button is toggled on or off
            var isBold = $(this).hasClass('active');

            // Toggle the font-weight style for the selected input field
            $(selectedInput).css('font-weight', isBold ? 'normal' : 'bold');

            // Toggle the "active" class to indicate the button state
            $(this).toggleClass('active', !isBold);
        }
    });

    // ITALIC BUTTON
    $('.italicBtn').on('click', function () {
        if (selectedInput) {
            // Check if the italic button is toggled on or off
            var isItalic = $(this).hasClass('active');

            // Toggle the font-style style for the selected input field
            $(selectedInput).css('font-style', isItalic ? 'normal' : 'italic');

            // Toggle the "active" class to indicate the button state
            $(this).toggleClass('active', !isItalic);
        }
    });

    // UNDERLINE BUTTON
    $('.underlineBtn').on('click', function () {
        if (selectedInput) {
            // Check if the underline button is toggled on or off
            var isUnderline = $(this).hasClass('active');

            // Toggle the text-decoration style for the selected input field
            $(selectedInput).css('text-decoration', isUnderline ? 'none' : 'underline');

            // Toggle the "active" class to indicate the button state
            $(this).toggleClass('active', !isUnderline);
        }
    });

    //COLOR BUTTON

    $('.colorBtn').spectrum({
        preferredFormat: "rgb",
        showPalette: true,
        palette: [
          ["#000", "#fff", "#ff0000", "#00ff00", "#0000ff"], // Background color palette
          //["#000", "#fff", "#ff0000", "#00ff00", "#0000ff"], // Text color palette
        ],
        change: function (color) {
          var selectedColor = color.toHexString();
          
          // Set background color and text color for all input fields
          $(selectedInput).css({
            "background-color": selectedColor,
            //"color": selectedColor === "#000" ? "#fff" : "#000", // Set text color based on background color
          });
        },
      });




      /*//COLOR BUTTON FOR SELECTED

      $('.colorBtn').spectrum({
        preferredFormat: "rgb",
        showPalette: true,
        palette: [
          ["#000", "#fff", "#ff0000", "#00ff00", "#0000ff"], // Background color palette
          //["#000", "#fff", "#ff0000", "#00ff00", "#0000ff"], // Text color palette
        ],
        change: function (color) {
          var selectedColor = color.toHexString();
          
          // Set background color and text color for all input fields
          $('input[id = "R12"]').css({
            "background-color": selectedColor,
            //"color": selectedColor === "#000" ? "#fff" : "#000", // Set text color based on background color
          });
        },
      });*/


      //SAVE BUTTON

      $('.downloadBtn').on('click',function(){
        $('#content').printThis();

      });

      



      //RESET BUTTON

      $('#resetButton').on('click', function () {
        // Get all input fields with class "activity-input"
        var activityInputs = $('input[type="text"]');

        // Clear the values of all input fields
        activityInputs.val('');

        // Clear the styles (bold, italic, underline)
        activityInputs.css({
            'font-weight': 'normal',
            'font-style': 'normal',
            'text-decoration': 'none',
            'background-color': 'white'
        });

        // Remove the "active" class from the style buttons
        $('.boldBtn, .italicBtn, .underlineBtn').removeClass('active');
    });

    //AI GENERATED TABLE FORM

    $('#addSubject').click(function () {
      var numSubjects = $('#numSubjects').val();
      for (var i = 1; i <= numSubjects; i++) {
          var subjectDiv = '<div class="form-group">' +
              '<label for="subjectName' + i + '">Name of Subject ' + i + ':</label>' +
              '<input type="text" class="form-control" id="subjectName' + i + '" name="subjectName[]" required>' +
              '</div>' 
          $('#subjectFields').append(subjectDiv);
      }
  });

  $('.toggle-section-ai').hide();
  $('.toggle-section-manual').hide();

  //TOGGLING AND RESETTING 

  function resetManualTimetableSection() {
    // Clear the values of all input fields in the manual timetable section
    $('#manual-time-table input[type="text"]').val('');
    // Clear the styles (bold, italic, underline)
    $('#manual-time-table input[type="text"]').css({
        'font-weight': 'normal',
        'font-style': 'normal',
        'text-decoration': 'none',
        'background-color': 'white'
    });
    // Remove the "active" class from the style buttons
    $('#manual-time-table .boldBtn, #manual-time-table .italicBtn, #manual-time-table .underlineBtn').removeClass('active');
}

// Function to reset the AI-generated timetable section
function resetAITimetableSection() {
    // Clear the values of input fields in the AI-generated timetable section
    $('#ai-generated input[type="number"]').val('');
    $('#ai-generated input[type="text"]').val('');
}

// Function to reset and hide the other section when one button is clicked
function resetAndHideOtherSection(currentTarget, otherTarget) {
    // Hide the other section
    $('#' + otherTarget).hide();

    // Reset the other section, if needed
    if (currentTarget === 'manual-time-table') {
        resetAITimetableSection(); // Reset AI-generated timetable section
    } else if (currentTarget === 'ai-generated') {
        resetManualTimetableSection(); // Reset manual timetable section
    }
}

  $('.toggleBtn1').click(function () {
    var target = $(this).data('target');
    // Hide all sections with class "toggle-section"
    $('.toggle-section-ai').hide();
    //resetAndHideOtherSection(target, 'ai-generated');
    // Show the selected section
    $('#' + target).show();
});

$('.toggleBtn2').click(function () {
    var target = $(this).data('target');
    // Hide all sections with class "toggle-section"
    $('.toggle-section-manual').hide();
    //resetAndHideOtherSection(target, 'manual-time-table');
    // Show the selected section
    $('#' + target).show();
});

//RESET THE AI GENERATED FORM 

$('#resetForm').on('click', function () {
  // Reset the form by clearing input values and hiding any error messages
  $('#duration, #numSubjects,#days,#preferredStartTiming,#preferredEndTiming').val('');
  $('#subjectFields').empty();
});

//RESET THE MANUAL TIME TABLE FORM

$('#resetManualTable').on('click', function () {
    // Remove all rows from the tbody
    $('#tbody').empty();
    // Clear the input values and reset styles for the manual timetable
    $('.boldBtn, .italicBtn, .underlineBtn').removeClass('active');
    $('input[type="text"]').css({
        'font-weight': 'normal',
        'font-style': 'normal',
        'text-decoration': 'none',
        'background-color': 'white'
    });
});








    


  });