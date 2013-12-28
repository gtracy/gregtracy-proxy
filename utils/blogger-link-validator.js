var request = require('request');

var site_id = 7963;
var grab_post_page = function(page) {
    request.get({
        url: 'http://posterous.com/api/2/sites/'+site_id+'/posts/public?page='+page,
        headers: {
            'Content-Type': 'application/json'
        }
    }, function(error, response, body) {
        if(error) {
            console.log('Error: '+error);
            not_done = false;
            return;
        }
        var data;
        try {
            data = JSON.parse(body);
        } catch (err) {
            console.log('Unable to fetch posts : '+err);
            console.dir(body);
        }
        if (data) {
            if( data.length === 0 ) {
                return;
            } else {
                data.forEach(function(p) {
                    // display_date: 2011/11/25 07:33:00 -0800
                    var ddate = p.display_date;
                    var sdate = ddate.substr(0,4) + '/' + ddate.substr(5,2);
                    console.log("'"+p.slug+"' : '"+p.slug+"',");
                });
                grab_post_page(++page);
            }
        }
    });
};

console.log("slugs = {");
grab_post_page(1);
