import re
import locale

from flask import url_for

locale.setlocale(locale.LC_ALL, '')

# template vars for pagination results counts and
# next/prev links on tabular views
def generate_pagination_values(c, params, url, data_type):
    pagination = {}
    per_page = int(c['pagination']['per_page'])
    page = int(c['pagination']['page'])
    current_results_start = per_page * (page - 1) + 1 
    current_results_end = per_page * page
    total_pages = int(c['pagination']['pages'])

    pagination['results_count'] = c['pagination']['count']
    pagination['page'] = page
    pagination['per_page'] = per_page
    pagination['current_results_start'] = current_results_start
    pagination['current_results_end'] = current_results_end

    if current_results_start or current_results_end:
        pagination['results_range'] = True

    # next url
    if page < total_pages:
        next_page_num = str(page + 1)
        params['page'] = next_page_num
        pagination['next_url'] = url_for(data_type, **params) 
        pagination['pagination_links'] = True

    # prev url
    if page - 1 > 0:
        prev_page_num = str(page - 1)
        params['page'] = prev_page_num
        pagination['prev_url'] = url_for(data_type, **params) 
        pagination['pagination_links'] = True

    return pagination

# maps basic values for candidates
def map_candidate_table_values(c):
    candidate = {
        'name': c['name']['full_name'],
        'office': c['elections'][0]['office_sought_full'],
        'election': int(c['elections'][0]['election_year']),
        'party': c['elections'][0]['party_affiliation'],
        'state': c['elections'][0]['state'],
        'district': int(c['elections'][0]['district']) 
            if c['elections'][0]['district'] else '',
        'nameURL': '/candidates/' + c['candidate_id'],
        'id': c['candidate_id']
    }

    return candidate

# maps basic values for committees
def map_committee_table_values(c):
    committee = {}

    if c.get('description'):
        committee['name'] = c['description'].get('name', '')
        committee['organization'] = c['description'].get(
            'organization_type_full', '')

    if c.get('treasurer'):
        committee['treasurer'] = c['treasurer'].get('name_full', '')

    if c.get('address'):
        committee['state'] = c['address'].get('state')

    if c.get('status'):
        committee['type'] = c['status'].get('type_full', '')
        committee['designation'] = c['status'].get(
            'designation_full', '')

    committee['nameURL'] ='/committees/' + c.get('committee_id', '')
    committee['id'] = c.get('committee_id', '')

    return committee

# maps committee values shown on candidate pages
def _map_committee_values(ac):
    c = {}
    c['id'] = ac.get('committee_id', '') 
    c['name'] = ac.get('committee_name', '')
    c['designation'] = ac.get('designation_full', '')
    c['designation_code'] = ac.get('designation', '')
    c['url'] = '/committees/' + ac.get('committee_id', '')
    return c

# maps totals to be shown on candidate and committee pages
def map_totals(t):
    reports = t['results'][0]['reports'][0]
    totals = t['results'][0]['totals'][0]
    totals_mapped = {}
    value_map = {
        'total_receipts': totals.get('receipts'),
        'total_disbursements': totals.get('total_disbursements'),
        'total_cash': reports.get('cash_on_hand_end_period'),
        'total_debt': reports.get('debts_owed_by_committee')
    }

    # format totals data in US dollars
    for v in value_map:
        if value_map[v]:
            totals_mapped[v] = locale.currency(
            value_map[v], grouping=True)
        else:
            totals_mapped[v] = 'unavailable'

    totals_mapped['report_year'] = str(int(reports['report_year']))

    # "calculated from" on site
    if reports.get('election_cycle'):
        cycle_minus_one = str(int(reports['election_cycle']) - 1)
        totals_mapped['years_totals'] = cycle_minus_one 
        totals_mapped['years_totals'] += ' - ' 
        totals_mapped['years_totals'] += str(reports['election_cycle'])

    # "source:" on site
    if reports.get('report_type_full'):
        totals_mapped['report_desc'] = re.sub('{.+}', 
            '', reports['report_type_full']) 

    return totals_mapped

# we want to show the committees on their related candidate 
# pages in this order, with primary committees on top
committee_type_map = {
    'A': 'authorized_committees',
    'D': 'leadership_committees',
    'J': 'joint_committees'
}

def map_candidate_page_values(c):
    candidate = map_candidate_table_values(c)

    if c.get('elections'):
        c_e = c['elections'][0]
        candidate['incumbent_challenge'] = c_e.get(
            'incumbent_challenge_full', '')
        if c_e.get('primary_committee'):
            candidate['primary_committee'] = _map_committee_values(
                c_e['primary_committee'])
            candidate['related_committees'] = True

        # affiliated committees = committee_type_map, 
        # plus more we ignore for the candidate pages
        if c_e.get('affiliated_committees'):
            candidate['affiliated_committees'] = []
            for i in range(len(c_e['affiliated_committees'])):
                candidate['affiliated_committees'].append(
                    _map_committee_values(c_e[
                        'affiliated_committees'][i]))

            candidate['authorized_committees'] = []
            candidate['leadership_committees'] = []
            candidate['joint_committees'] = []

            for i in range(len(candidate['affiliated_committees'])):
                cmte = candidate['affiliated_committees'][i]
                cmte_type = cmte['designation_code']
                # drop anything that's not of the types we're
                # interested in
                if (cmte_type in committee_type_map):
                    candidate[committee_type_map[
                        cmte_type]].append(cmte)
                    candidate['related_committees'] = True

    return candidate

def map_committee_page_values(c):
    committee = map_committee_table_values(c)

    if c.get('address'):
        committee['address'] = {
            'state': c['address'].get('state'),
            'zip': c['address'].get('zip'),
            'city': c['address'].get('city'),
            'street_1': c['address'].get('street_1'),
            'street_2': c['address'].get('street_2')
        }

    return committee

type_map = {
    'candidates': map_candidate_table_values,
    'candidate': map_candidate_page_values,
    'committees': map_committee_table_values,
    'committee': map_committee_page_values
}
