$(function(){
    //original field values
    var field_values = {
            //id        :  value
            'firstname'  : 'first name',
            'password'  : 'password',
            'cpassword' : 'password',
            'mothername'  : "mother's name",
            'lastname'  : 'last name',
            'email'  : 'email address',
            'fathername' : "father's name",
            'dob':'dd/mm/yy',
            'address':'address',
            'pnum':'',
            'school':'school name',
            'sclass':'',
            'company':'Abcus/Vedic Math Company',
            'tsize':"",
            'simage':'student image',
            'mpe':'',
            'exam_group':'',
            'sname':'',
            'choices':'',
            'sec_name':'',
            'choices1':'',
            'workshop':''

    };
    var field_values1 = {
            'regnum'  : 'registration number',
            'paasword2'  : 'password',
            'cpaasword'  : 'password',
            

    };

    //inputfocus
    $('input#firstname').inputfocus({ value: field_values['firstname'] });
    $('input#password').inputfocus({ value: field_values['password'] });
    $('input#cpassword').inputfocus({ value: field_values['cpassword'] }); 
    $('input#lastname').inputfocus({ value: field_values['lastname'] });
    $('input#mothername').inputfocus({ value: field_values['mothername'] });
    $('input#email').inputfocus({ value: field_values['email'] }); 
    $('input#fathername').inputfocus({ value: field_values['fathername'] }); 
    $('input#dob').inputfocus({ value: field_values['dob'] });
    $('input#address').inputfocus({ value: field_values['address'] });
    $('input#pnum').inputfocus({ value: field_values['pnum'] }); 
    $('input#school').inputfocus({ value: field_values['school'] });
    $('input#company').inputfocus({ value: field_values['company'] });

    $('input#regnum').inputfocus({ value: field_values1['regnum'] });
    $('input#password2').inputfocus({ value: field_values1['password2'] });
    $('input#cpassword1').inputfocus({ value: field_values1['cpassword1'] });
   



    //reset progress bar
    $('#progress').css('width','0');
    $('#progress_text').html('0% Complete');

    //first_step
    $('form').submit(function(){ return false; });
    $('#submit_first').click(function(){
        //remove classes
        $('#first_step input').removeClass('error').removeClass('valid');

        //ckeck if inputs aren't empty
        var fields = $('#first_step input[type=text], #first_step input[type=password]');
        var error = 0;
        fields.each(function(){
            var value = $(this).val();
            if( value.length<4 || value==field_values[$(this).attr('id')] ) {
                $(this).addClass('error');
                $(this).effect("shake", { times:3 }, 50);
                
                error++;
            } else {
                $(this).addClass('valid');
            }
        });        
        
        if(!error) {
            if( $('#password').val() != $('#cpassword').val() ) {
                    $('#first_step input[type=password]').each(function(){
                        $(this).removeClass('valid').addClass('error');
                        $(this).effect("shake", { times:3 }, 50);
                    });
                    
                    return false;
            } else {   
                //update progress bar
                $('#progress_text').html('33% Complete');
                $('#progress').css('width','113px');
                
                //slide steps
                $('#first_step').slideUp();
                $('#second_step').slideDown();     
            }               
        } else return false;
    });


    $('#submit_second').click(function(){
        //remove classes
        $('#second_step input').removeClass('error').removeClass('valid');

        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;  
        var fields = $('#second_step input[type=text]');
        var error = 0;
        fields.each(function(){
            var value = $(this).val();
            if( value.length<1 || value==field_values[$(this).attr('id')] || ( $(this).attr('id')=='email' && !emailPattern.test(value) ) ) {
                $(this).addClass('error');
                $(this).effect("shake", { times:3 }, 50);
                
                error++;
            } else {
                $(this).addClass('valid');
            }
        });

        if(!error) {
                //update progress bar
                $('#progress_text').html('66% Complete');
                $('#progress').css('width','226px');
                
                //slide steps
                $('#second_step').slideUp();
                $('#third_step').slideDown();     
        } else return false;

    });


    $('#submit_third').click(function(){
        //update progress bar
        $('#progress_text').html('100% Complete');
        $('#progress').css('width','339px');

        //prepare the fourth step
        var fields = new Array(
            $('#firstname').val() + ' ' + $('#lastname').val(),
            $('#fathername').val(),
            $('#mothername').val(),
            $('#password').val(),
            $('#gender').val(),
            $('#tsize').val(),
            $('#email').val(),
            $('#address').val(),
            $('#pnum').val(), 
            $('#school').val(),
            $('#sclass').val(),
            $('#mpe').val(),
            $('#company').val(),
            $('#exam_group').val(),
            $('#choices').val(),
            $('#choices1').val()

        );
        var tr = $('#fourth_step tr');
        tr.each(function(){
            //alert( fields[$(this).index()] )
            $(this).children('td:nth-child(2)').html(fields[$(this).index()]);
        });
                
        //slide steps
        $('#third_step').slideUp();
        $('#fourth_step').slideDown();            
    });


    $('#submit_fourth').click(function(){
        //send information to server
        //alert('Data sent');

document.forms["form"].submit();
    });

}); 
 $('#submit_forget').click(function(){
        //send information to server
        window.location.href="forget_password1.html";
       // alert('Data sent');
    });
    $('#submit_forget1').click(function(){
        //send information to server
        window.location.href="forget_password2.html";
       // alert('Data sent');
    });
    $('#submit_forget2').click(function(){
        //send information to server
        window.location.href="login.html";
       // alert('Data sent');
    });


//login


