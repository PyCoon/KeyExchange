{% extends "base.tpl" %}

{% block content %}

<script type="text/javascript">


message="{{message}}";
alert(message);
document.location.href = "{% url "front_page" %}";
</script>
{% endblock %}


{{message}}
