$(document).ready(function(){

        var launch_query = function(){

            var term = $.trim($("#id_test_query").val());
            var start_lang = $.trim($("#startlang-selector").val());
            var trans_lang = $.trim($("#translang-selector").val());
            // TODO: Improve validation for client
            if(term != "" && start_lang != "" && trans_lang != ""){
                var request = {};
                request['term'] = term;
                request['start_lang'] = start_lang;
                request['trans_lang'] = trans_lang;
                $.ajax({url:'blob', data:request, dataType:"json"}).done(function(data){ display_items(data); });
            }
            return false;
        }

        var display_items = function(data){

            alert(data);


        }

    $("#submit").click(launch_query)











})