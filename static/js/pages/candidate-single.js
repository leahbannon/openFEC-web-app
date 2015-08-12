var tables = require('../modules/tables');
var URI = require('URIjs');

var events = require('../modules/events');

var filingsColumns = [
  {
    data: 'document_description',
    className: 'all',
    orderable: false,
    render: function(data, type, row, meta) {
      var anchor = document.createElement('a');
      anchor.textContent = data;
      anchor.setAttribute('href', row.pdf_url);
      anchor.setAttribute('target', '_blank');
      return anchor.outerHTML;
    }
  },
  {
    data: 'amendment_indicator',
    className: 'min-desktop',
    render: function(data, type, row, meta) {
      if (data === 'A') {
        data = 'Amended';
      } else if (data === 'N') {
        data = 'New';
      } else {
        data = '';
      }
      return data;
    },
  },
  tables.dateColumn({data: 'receipt_date', className: 'min-tablet'}),
  tables.dateColumn({data: 'coverage_end_date', className: 'min-tablet', orderable: false}),
  tables.currencyColumn({data: 'total_receipts', className: 'min-tablet'}),
  tables.currencyColumn({data: 'total_disbursements', className: 'min-tablet'}),
  tables.currencyColumn({data: 'total_independent_expenditures', className: 'min-tablet'}),
];

$(document).ready(function() {
  // Set up data tables
  $('.data-table').each(function(index, table) {
    var $table = $(table);
    var candidateId = $table.attr('data-candidate');
    var cycle = $table.attr('data-cycle');
    var year = $table.attr('data-year');
    var path, query;
    switch ($table.attr('data-type')) {
        case 'filing':
        var $form = $('#category-filters');
        tables.initTableDeferred($table, $form, 'filings/', {candidate_id: candidateId}, filingsColumns, tables.offsetCallbacks, {
          dom: 't<"results-info results-info--bottom meta-box"lfrip>',
          // Order by receipt date descending
          order: [[4, 'desc']],
        });
    }
  });

function buildStateUrl($elm) {
  return URI(API_LOCATION)
    .path([
      API_VERSION,
    ].join('/'))
    .query({
      cycle: $elm.data('cycle'),
      per_page: 99
    })
    .toString();
}


});