import React, { Component } from "react";
import PropTypes from "prop-types";
import Layout from "../Layout";
import { withRouter } from "react-router-dom";
import { Modal, ModalBody } from "reactstrap";
import Select from "react-select";
import BaseActions from "../../../actions/BaseActions";
import Preview from "./Preview";
import Loading from "../../common/Loading";
import Schedule from "./Schedule";

const ModelEvaluation = props => {
  const [dates, setDates] = React.useState([]);
  const [selectedDates, setSelectedDates] = React.useState([]);
  const [loadingEval, setLoadingEval] = React.useState(true);
  const [loading, setLoading] = React.useState(false);
  const [evaluations, setEvaluations] = React.useState([]);
  const [firstReload, setFirstReload] = React.useState(true);

  const reload = () => {
    setLoadingEval(true);
    // BaseActions.get("dates/target").then(result => {
    //   if (result.data) {
    //     let values = [];
    //     result.data.forEach(item => {
    //       values.push({
    //         value: item,
    //         label: item
    //       });
    //     });
    //     setDates(values);
    //   }

    //   if (firstReload === true) {
    //     let data = {
    //       eval_period_datetimes: result.data
    //     };

    //     const body = JSON.stringify(data);

    //     BaseActions.postJSONFile("files/performance", "config.json", body)
    //       .then(response => {
    //         setFirstReload(false);
    //         BaseActions.get("evaluations").then(resultEvaluations => {
    //           setLoadingEval(false);
    //           if (resultEvaluations.data) {
    //             setEvaluations(resultEvaluations.data);
    //           }
    //         });
    //       })
    //       .catch(error => {
    //         setFirstReload(false);
    //         BaseActions.get("evaluations").then(resultEvaluations => {
    //           setLoadingEval(false);
    //           if (resultEvaluations.data) {
    //             setEvaluations(resultEvaluations.data);
    //           }
    //         });
    //       });
    //   } else {
    //     BaseActions.get("evaluations")
    //       .then(resultEvaluations => {
    //         setLoading(false);
    //         if (resultEvaluations.data) {
    //           setEvaluations(resultEvaluations.data);
    //         }
    //       })
    //       .catch(error => {
    //         setLoading(false);
    //       });
    //   }
    // });

    BaseActions.getFromApiary(
      "projects/" + props.location.state.project.name + "/metrics"
    ).then(result => {
      if (result) {
        setEvaluations(result);
        setLoadingEval(false);
      }
    });
  };

  React.useEffect(() => {
    reload();
  }, []);

  const onChangeDate = date => {
    let foundValue = selectedDates.includes(date);

    setSelectedDates(prevSelectedDates =>
      foundValue === false
        ? [...prevSelectedDates, date]
        : prevSelectedDates.filter(
            prevSelectedDate => prevSelectedDate.value !== date.value
          )
    );
  };

  const onClickLoadResults = () => {
    setLoading(true);
    const eval_period_datetimes = selectedDates.map(date => {
      return date.value;
    });

    let data = {
      eval_period_datetimes: eval_period_datetimes
    };

    const body = JSON.stringify(data);

    BaseActions.postJSONFile("files/performance", "config.json", body)
      .then(response => {
        setLoading(false);
        reload();
      })
      .catch(e => {
        setLoading(false);
      });
  };
  return (
    <Layout tab={props.tab} title="Model Evaluation">
      <Schedule />
      {loadingEval === false ? (
        <div className="container-evaluation">
          <div className="container-top-section">
            <div className="container-num-metrics">
              <p>
                <span>NUMBER OF DASHBOARD METRICS: {evaluations.length}</span>
              </p>
            </div>
            {/* <div className="container-filters">
              <div className="model-performance-filter">
                <p>Time Period:</p>
                <Select
                  className="model-performance-select"
                  value={selectedDates}
                  onChange={onChangeDate}
                  options={dates}
                  closeMenuOnSelect={false}
                />
                {loading === true ? (
                  <button
                    type="button"
                    className="b--mat b--affirmative text-upper button-load-results"
                    disabled
                  >
                    loading...
                  </button>
                ) : (
                  <button
                    type="button"
                    className="b--mat b--affirmative text-upper button-load-results"
                    onClick={onClickLoadResults}
                  >
                    load results
                  </button>
                )}
              </div>
            </div> */}
          </div>
          {evaluations.length > 0 ? (
            <div className="container-eval-content">
              {evaluations.map((evaluation, i) => {
                return <Preview evaluation={evaluation} />;
              })}
            </div>
          ) : (
            <div className="container-eval-empty">
              <p>It's a fresh start.</p>
              <p>There are currently no metrics to look at.</p>
            </div>
          )}
        </div>
      ) : (
        <Loading loadingMessage="We are currently loading your evaluations" />
      )}
    </Layout>
  );
};

ModelEvaluation.propTypes = {
  tab: PropTypes.string
};

ModelEvaluation.defaultProps = {
  tab: "Evaluation"
};

export default withRouter(ModelEvaluation);
