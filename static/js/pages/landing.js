'use strict';

/* global require, document */

var $ = require('jquery');

var tables = require('../modules/tables');
var columns = require('../modules/columns');
var lookup = require('../modules/election-lookup');
var summary = require('../modules/election-summary');

var filingsColumns = columns.getColumns(
  columns.filings,
  ['pdf_url', 'filer_name', 'receipt_date']
);

$(document).ready(function() {
  var $table = $('#results');
  tables.initTable($table, null, 'filings', {per_page: 10}, filingsColumns, tables.offsetCallbacks, {
    // Order by receipt date descending
    order: [[2, 'desc']],
    useFilters: false,
    dom: 't'
  });

  new lookup.ElectionLookupPreview('#election-preview');
  new summary.ElectionSummary('#election-summary', {cycle: 2016, office: 'president'});
});
