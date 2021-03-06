'use strict';

/* global require, document */

var $ = require('jquery');
var _ = require('underscore');

var tables = require('../modules/tables');
var helpers = require('../modules/helpers');
var donationTemplate = require('../../templates/receipts.hbs');

var columns = [
  {
    data: 'contributor',
    orderable: false,
    className: 'all',
    width: '200px',
    render: function(data, type, row, meta) {
      if (data) {
        return tables.buildEntityLink(
          data.name,
          helpers.buildAppUrl(['committee', data.committee_id]),
          'committee'
        );
      } else {
        return row.contributor_name;
      }
    }
  },
  {data: 'contributor_state', orderable: false, className: 'min-desktop hide-panel'},
  {data: 'contributor_employer', orderable: false, className: 'min-desktop hide-panel'},
  tables.currencyColumn({data: 'contribution_receipt_amount', className: 'min-tablet'}),
  tables.dateColumn({data: 'contribution_receipt_date', className: 'min-tablet hide-panel-tablet'}),
  {
    data: 'committee',
    orderable: false,
    className: 'min-desktop hide-panel',
    width: '250px',
    render: function(data, type, row, meta) {
      if (data) {
        return tables.buildEntityLink(
          data.name,
          helpers.buildAppUrl(['committee', data.committee_id]),
          'committee'
        );
      } else {
        return '';
      }
    }
  },
  {
    className: 'all u-no-padding',
    width: '20px',
    orderable: false,
    render: function(data, type, row, meta) {
      return tables.MODAL_TRIGGER_HTML;
    }
  }
];

$(document).ready(function() {
  var $table = $('#results');
  var $form = $('#category-filters');
  tables.initTable(
    $table,
    $form,
    'schedules/schedule_a',
    {},
    columns,
    _.extend(tables.seekCallbacks, {
      afterRender: tables.modalRenderFactory(donationTemplate)
    }),
    {
      order: [[4, 'desc']],
      pagingType: 'simple',
      useFilters: true,
      rowCallback: tables.modalRenderRow
    }
  );
});
