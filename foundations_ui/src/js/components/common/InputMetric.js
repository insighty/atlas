import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { ScrollSyncPane } from 'react-scroll-sync';
import TableSectionHeader from './TableSectionHeader';
import CommonActions from '../../actions/CommonActions';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.changeHiddenParams = this.changeHiddenParams.bind(this);
    this.updateSearchText = this.updateSearchText.bind(this);
    this.hasNoRows = this.hasNoRows.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: [],
      allInputParams: this.props.allInputParams,
      jobs: [],
      isMetric: this.props.isMetric,
      searchText: '',
      toggleNumberFilter: this.props.toggleNumberFilter,
      filteredArray: this.props.filters,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      allInputParams: nextProps.allInputParams,
      jobs: nextProps.jobs,
      filteredArray: nextProps.filters,
    });
  }

  changeHiddenParams(hiddenParams) {
    this.setState({ hiddenInputParams: hiddenParams });
    this.forceUpdate();
  }

  updateSearchText(text) {
    this.setState({ searchText: text });
    this.forceUpdate();
  }

  hasNoRows(rows, flatParams) {
    const { hiddenInputParams } = this.state;
    return rows === null || rows.length === 0 || flatParams.length === hiddenInputParams.length;
  }

  render() {
    const {
      header, hiddenInputParams, allInputParams, jobs, isMetric, searchText, toggleNumberFilter, filteredArray,
    } = this.state;

    const flatParams = CommonActions.getFlatArray(allInputParams);

    const inputParams = CommonActions.getInputMetricColumnHeaders(
      allInputParams, hiddenInputParams, toggleNumberFilter, isMetric, filteredArray,
    );
    let rows = CommonActions.getInputMetricRows(jobs, isMetric, flatParams, hiddenInputParams);
    if (this.hasNoRows(rows, flatParams)) {
      rows = [];
      rows.push(<p key="no-rows-message" className="empty-columns-message">There are no columns selected.</p>);
    }

    return (
      <div className="job-static-columns-container">
        <TableSectionHeader
          header={header}
          changeHiddenParams={this.changeHiddenParams}
          columns={allInputParams}
          hiddenInputParams={hiddenInputParams}
          updateSearchText={this.updateSearchText}
          searchText={searchText}
          isMetric={isMetric}
        />
        <div className="input-metric-header-row-container">
          <div className="input-metric-column-container column-header">
            {inputParams}
          </div>
          <ScrollSyncPane group="vertical">
            <div className="input-metric-column-container">
              {rows}
            </div>
          </ScrollSyncPane>
        </div>
      </div>
    );
  }
}

InputMetric.propTypes = {
  header: PropTypes.string,
  hiddenInputParams: PropTypes.array,
  allInputParams: PropTypes.array,
  jobs: PropTypes.array,
  cellWidths: PropTypes.array,
  isMetric: PropTypes.bool,
  searchText: PropTypes.string,
  toggleNumberFilter: PropTypes.func,
  filters: PropTypes.array,
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: [],
  cellWidths: [],
  isMetric: false,
  searchText: '',
  toggleNumberFilter: () => {},
  filters: [],
};


export default InputMetric;