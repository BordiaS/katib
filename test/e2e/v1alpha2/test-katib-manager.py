import logging
import grpc
import api_pb2
import api_pb2_grpc

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TEST_TRIAL = "test_trial"
TEST_EXPERIMENT = "test_experiment"

def register_experiment(stub):
  obj = api_pb2.ObjectiveSpec(type=1, goal=0.09, objective_metric_name="loss")
  algo = api_pb2.AlgorithmSpec(algorithm_name="random")
  exp_spec = api_pb2.ExperimentSpec(objective=obj,
                                    algorithm=algo,
                                    trial_template="run-mnist",
                                    parallel_trial_count=2,
                                    max_trial_count=9,
                                    metrics_collector_type='2')
  exp_status = api_pb2.ExperimentStatus(condition=1,
                                        start_time="2019-04-28T14:09:15Z",
                                        completion_time="2019-04-28T16:09:15Z")
  exp = api_pb2.Experiment(experiment_spec=exp_spec,
                           name=TEST_EXPERIMENT,
                           experiment_status=exp_status)
  try:
    stub.RegisterExperiment(api_pb2.RegisterExperimentRequest(experiment=exp), 10)
    logger.info("Register experiment %s successfully" % TEST_EXPERIMENT)
  except:
    logger.error("Failed to Register experiment", exc_info=True)
    raise

def update_experiment_status(stub):
  try:
    new = api_pb2.ExperimentStatus(condition=2,start_time="2019-04-28T17:09:15Z",completion_time="2019-04-28T18:09:15Z")
    stub.UpdateExperimentStatus(api_pb2.UpdateExperimentStatusRequest(experiment_name=TEST_EXPERIMENT, new_status=new),10)
    logger.info("Update status of experiment %s successfully" % TEST_EXPERIMENT)
  except:
    logger.error("Fail to update status of experiment", exc_info=True)
    raise

def get_experiment(stub):
  try:
    exp = stub.GetExperiment(api_pb2.GetExperimentRequest(experiment_name=TEST_EXPERIMENT), 10)
    if exp and exp.experiment.name == TEST_EXPERIMENT:
      logger.info("Get experiment %s successfully" % TEST_EXPERIMENT)
    else:
      raise Exception()
  except:
    logger.error("Failed to get experiment %s" % TEST_EXPERIMENT, exc_info=True)
    raise

def delete_experiment(stub):
  try:
    stub.DeleteExperiment(api_pb2.DeleteExperimentRequest(experiment_name=TEST_EXPERIMENT), 10)
    logger.info("Delete experiment %s successfully" % TEST_EXPERIMENT)
  except:
    logger.error("Failed to delete experiment %s" % TEST_EXPERIMENT, exc_info=True)
    raise

def register_trial(stub):
  try:
    parameters = api_pb2.TrialSpec.ParameterAssignments(assignments=[api_pb2.ParameterAssignment(name="rl", value="0.01")])
    spec = api_pb2.TrialSpec(experiment_name=TEST_EXPERIMENT,
                             run_spec="a batch/job resource",
                             parameter_assignments=parameters)
    observation = api_pb2.Observation(metrics=[api_pb2.Metric(name="loss", value="0.54")])
    status = api_pb2.TrialStatus(condition=2,
                                 observation=observation,
                                 start_time="2019-04-28T17:09:15Z",
                                 completion_time="2019-04-28T18:09:15Z")
    t = api_pb2.Trial(name=TEST_TRIAL, status=status, spec=spec)
    stub.RegisterTrial(api_pb2.RegisterTrialRequest(trial=t), 10)
    logger.info("Register trial %s successfully" % TEST_TRIAL)
  except:
    logger.error("Failed to register trial %s" % TEST_TRIAL, exc_info=True)
    raise

def get_trial(stub):
  try:
    reply = stub.GetTrial(api_pb2.GetTrialRequest(trial_name=TEST_TRIAL), 10)
    trial = reply.trial
    if trial and trial.name == TEST_TRIAL:
      logger.info("Get trial %s successfully" % TEST_TRIAL)
    else:
      raise Exception()
  except:
    logger.error("Failed to get trial %s" % TEST_TRIAL, exc_info=True)
    raise


def test():
  with grpc.insecure_channel('127.0.0.1:6789') as channel:
    stub = api_pb2_grpc.ManagerStub(channel)
    register_experiment(stub)
    get_experiment(stub)
    update_experiment_status(stub)
    register_trial(stub)
    get_trial(stub)
    delete_experiment(stub)
    try:
      get_trial(stub)
    except:
      return 0
    else:
      exit(1)

if __name__ == '__main__':
  test()
