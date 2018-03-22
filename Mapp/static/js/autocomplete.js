$(function() {
$("#new-user").autocomplete({
source: "/autocomplete/newuser/",
minLength: 2,
});
});
