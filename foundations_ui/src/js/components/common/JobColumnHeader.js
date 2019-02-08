import React, { Component } from 'react';
import PropTypes from 'prop-types';
import JobActions from '../../actions/JobListActions';
import Tooltip from './Tooltip';

class JobColumnHeader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      title: this.props.title,
      isStatus: this.props.isStatus,
      offsetDivClass: this.props.className,
      containerDivClass: this.props.containerClass,
      toggleFilter: this.props.toggleFilter,
      colType: this.props.colType,
      isMetric: this.props.isMetric,
      isFiltered: this.props.isFiltered,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState(
      {
        isFiltered: nextProps.isFiltered,
      },
    );
  }

  render() {
    const {
      title, isStatus, offsetDivClass, containerDivClass, toggleFilter, colType, isMetric, isFiltered,
    } = this.state;
    const headerClassName = JobActions.getJobColumnHeaderH4Class(isStatus);
    const arrowClassName = JobActions.getJobColumnHeaderArrowClass(isStatus, colType, isMetric);
    const divClassName = JobActions.getJobColumnHeaderDivClass(containerDivClass, isStatus);
    const presentationClassName = JobActions.getJobColumnHeaderPresentationClass(colType, isMetric);

    const tooltip = <Tooltip message={title} />;
    const filterIcon = isFiltered ? <div className="i--icon-filtered" /> : null;

    return (
      <div
        className={divClassName}
        ref={(c) => { this.headerContainer = c; }}
      >
        <div className={offsetDivClass}>
          <h4
            className={headerClassName}
          >
            {title}
          </h4>
          {tooltip}
          <div className="icon-container">
            {filterIcon}
          </div>
          <div role="presentation" onClick={toggleFilter} onKeyPress={toggleFilter} className={presentationClassName}>
            <div id={title} className={arrowClassName} />
          </div>
        </div>
      </div>
    );
  }
}

JobColumnHeader.propTypes = {
  title: PropTypes.string,
  isStatus: PropTypes.bool,
  className: PropTypes.string,
  containerClass: PropTypes.string,
  toggleFilter: PropTypes.func,
  colType: PropTypes.string,
  isMetric: PropTypes.bool,
  isFiltered: PropTypes.bool,
};

JobColumnHeader.defaultProps = {
  title: '',
  isStatus: false,
  className: '',
  containerClass: 'job-column-header',
  toggleFilter: () => {},
  colType: 'string',
  isMetric: false,
  isFiltered: false,
};

export default JobColumnHeader;