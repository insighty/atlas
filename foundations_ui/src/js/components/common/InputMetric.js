import React, { Component } from 'react';
import PropTypes from 'prop-types';
import TableSectionHeader from './TableSectionHeader';
import JobColumnHeader from './JobColumnHeader';
import InputMetricCell from './InputMetricCell';
import InputMetricRow from './InputMetricRow';
import CommonActions from '../../actions/CommonActions';

class InputMetric extends Component {
  constructor(props) {
    super(props);
    this.resizeCells = this.resizeCells.bind(this);
    this.isCellWidthSame = this.isCellWidthSame.bind(this);
    this.state = {
      header: this.props.header,
      hiddenInputParams: this.props.hiddenInputParams,
      allInputParams: this.props.allInputParams,
      jobs: [],
      cellWidths: new Array(this.props.allInputParams.length),
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      allInputParams: nextProps.allInputParams,
      jobs: nextProps.jobs,
      cellWidths: new Array(nextProps.allInputParams.length),
    });
  }

  resizeCells(colIndex, newWidth) {
    const { cellWidths } = this.state;
    if (this.isCellWidthSame(cellWidths[colIndex], newWidth)) {
      cellWidths[colIndex] = newWidth;
      this.forceUpdate();
    }
  }

  isCellWidthSame(oldWidth, newWidth) {
    return (oldWidth !== newWidth);
  }

  render() {
    const {
      header, hiddenInputParams, allInputParams, jobs, cellWidths,
    } = this.state;

    const inputParams = CommonActions.getInputMetricColumnHeaders(allInputParams, this.resizeCells);
    const rows = CommonActions.getInputMetricRows(jobs, cellWidths);

    return (
      <div className="input-metric-container">
        <TableSectionHeader header={header} />
        <div className="input-metric-column-header-container">
          {inputParams}
          {rows}
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
};

InputMetric.defaultProps = {
  header: '',
  hiddenInputParams: [],
  allInputParams: [],
  jobs: [],
  cellWidths: [],
};


export default InputMetric;
