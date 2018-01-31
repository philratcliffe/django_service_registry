from behave import given, then, when
from rest_framework import status


@given(u'there is an empty ServiceRegistry')
def check_empty_registry(context):
    from services.models import Service
    assert (Service.objects.all().count() == 0)


@given(u'a set of specific services')
def setup_db(context):
    from services.models import Service
    for row in context.table:
        s = Service(service=row['service'], version=row['version'])
        s.save()


@then(u'I should be notified with a change "{change}"')
def check_notification(context, change):
    if context.response.status_code == status.HTTP_201_CREATED:
        context.test.assertEqual(change, 'created')
    elif context.response.status_code == status.HTTP_204_NO_CONTENT:
        context.test.assertEqual(change, 'removed')
    elif context.response.status_code == status.HTTP_200_OK:
        context.test.assertEqual(change, 'changed')
    else:
        assert ("Error: unexpected response")


@when(u'I add a service "{service}" with version "{version}')
def add_service_with_version(context, service, version):
    create_url = context.get_url('list_or_add_endpoint')
    create_data = {'service': service, 'version': version}
    context.response = context.test.client.post(
        create_url, create_data, format='json')
    context.test.assertEqual(context.response.status_code,
                             status.HTTP_201_CREATED)


@when(u'I search for a service "{service}" with version "{version}"')
def step1_impl(context, service, version):
    find_url = context.get_url('find_or_delete_endpoint', **{
        'service': service,
        'version': version
    })
    context.response = context.test.client.get(find_url)


@when(u'I search for a service "{service}" without version')
def step2_impl(context, service):
    find_url = context.get_url('find_or_delete_endpoint', **{
        'service': service
    })
    context.response = context.test.client.get(find_url)


@when(u'I update a service')
def step3_impl(context):
    update_url = context.get_url('update_endpoint', **{'pk': 1})
    update_data = {
        'service': 'test-update',
        'version': '0.0.9',
    }
    context.response = context.test.client.put(
        update_url, update_data, format='json')


@when(u'I remove a service')
def step4_impl(context):
    remove_url = context.get_url('find_or_delete_endpoint', service='test')
    context.response = context.test.client.delete(remove_url)


@then(u'the service should be removed')
def step5_impl(context):
    context.test.assertEqual(context.response.status_code,
                             status.HTTP_204_NO_CONTENT)


@then(u'I should find count "{count}" instances of service')
def step6_impl(context, count):
    context.test.assertEqual(context.response.data['count'], int(count))


@then(u'I should find count "{count}" services')
def step7_impl(context, count):
    context.test.assertEqual(context.response.data['count'], int(count))


@then(u'the service "{service}" should have the correct type')
def step8_impl(context, service):
    context.test.assertEqual(context.response.data['service'], service)


@then(u'the service "{service}" should have the correct version "{version}"')
def step9_impl(context, service, version):
    context.test.assertEquals(context.response.data['version'], version)
