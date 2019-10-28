import React from "react";
import { get, put, del } from "./BaseActions";
import MonitorListTableRow from "../components/PackagePage/MonitorSchedules/MonitorListTableRow";
import MonitorJobTableRow from "../components/PackagePage/MonitorSchedules/MonitorJobTableRow";

const MonitorSchedulesActions = {
  getMonitorList: projectName => {
    const url = `projects/${projectName}/monitors`;

    return get(url)
      .then(results => {
        return results;
      })
      .catch(() => {
        return {};
      });
  },

  getRows: (results, onClickRow) => {
    const allMonitors = Object.keys(results);
    return allMonitors.map(monitor => {
      const key = results[monitor].properties.job_id + results[monitor].properties.metadata.username;
      return (
        <MonitorListTableRow
          key={key}
          onClick={onClickRow}
          monitorName={results[monitor].properties.job_id}
          status={results[monitor].status}
          user={results[monitor].properties.metadata.username}
        />
      );
    });
  },

  getMonitorJobs: (projectName, monitorName) => {
    const url = `projects/${projectName}/monitors/${monitorName}/jobs`;

    return get(url)
      .then(results => {
        return results;
      })
      .catch(() => {
        return {};
      });
  },

  getMonitorJobRows: results => {
    if (!results.error) {
      return results.map(job => {
        const key = job.job_id + job.duration;
        return (
          <MonitorJobTableRow
            key={key}
            jobID={job.job_id}
            status={job.status}
            launched={job.start_time}
            duration={job.completed_time}
          />
        );
      });
    }
  },

  resumeMonitor: (projectName, monitorName) => {
    const body = {
      status: "active"
    };

    return put(
      `projects/${projectName}/monitors/${monitorName}`,
      body
    );
  },

  pauseMonitor: (projectName, monitorName) => {
    const body = {
      status: "pause"
    };

    return put(
      `projects/${projectName}/monitors/${monitorName}`,
      body
    );
  },

  deleteMonitor: (projectName, monitorName) => {
    return del(`projects/${projectName}/monitors/${monitorName}`);
  }

};

export default MonitorSchedulesActions;
