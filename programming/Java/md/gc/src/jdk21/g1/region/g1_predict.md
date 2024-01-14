# 停顿预测模型

```cpp
//////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Policy.cpp //
//////////////////////////////////////////////////////////

void G1Policy::update_young_length_bounds() {
  assert(!Universe::is_fully_initialized() || SafepointSynchronize::is_at_safepoint(), "must be");
  bool for_young_only_phase = collector_state()->in_young_only_phase();
  update_young_length_bounds(_analytics->predict_pending_cards(for_young_only_phase),
                             _analytics->predict_rs_length(for_young_only_phase));
}

/////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Analytics.cpp //
/////////////////////////////////////////////////////////////

size_t G1Analytics::predict_pending_cards(bool for_young_only_phase) const {
  return predict_size(&_pending_cards_seq, for_young_only_phase);
}

size_t G1Analytics::predict_rs_length(bool for_young_only_phase) const {
  return predict_size(&_rs_length_seq, for_young_only_phase);
}

size_t G1Analytics::predict_size(G1PhaseDependentSeq const* seq, bool for_young_only_phase) const {
  return (size_t)predict_zero_bounded(seq, for_young_only_phase);
}

double G1Analytics::predict_zero_bounded(G1PhaseDependentSeq const* seq, bool for_young_only_phase) const {
  return MAX2(seq->predict(_predictor, for_young_only_phase), 0.0);
}

/////////////////////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1AnalyticsSequences.inline.hpp //
/////////////////////////////////////////////////////////////////////////////

double G1PhaseDependentSeq::predict(const G1Predictions* predictor, bool use_young_only_phase_seq) const {
  if (use_young_only_phase_seq || !enough_samples_to_use_mixed_seq()) {
    // 预测只作Young GC时新生代所需region数
    return predictor->predict(&_young_only_seq);
  } else {
    // 预测Mixed GC时新生代所需region数
    return predictor->predict(&_mixed_seq);
  }
}

///////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Predictions.hpp //
///////////////////////////////////////////////////////////////

// Utility class containing various helper methods for prediction.
class G1Predictions {
 private:
  double _sigma;

  // This function is used to estimate the stddev of sample sets. There is some
  // special consideration of small sample sets: the actual stddev for them is
  // not very useful, so we calculate some value based on the sample average.
  // Five or more samples yields zero (at that point we use the stddev); fewer
  // scale the sample set average linearly from two times the average to 0.5 times
  // it.
  double stddev_estimate(TruncatedSeq const* seq) const {
    // dsd(): 衰减标准差
    double estimate = seq->dsd();
    // seq->num(): seq中的元素数量
    int const samples = seq->num();
    if (samples < 5) {
      estimate = MAX2(seq->davg() * (5 - samples) / 2.0, estimate);
    }
    return estimate;
  }
 public:
  // 调用位置
  // G1ConfidencePercent: 默认50
  //
  // G1Policy::G1Policy(STWGCTimer* gc_timer) :
  //   _predictor(G1ConfidencePercent / 100.0),
  // }
  //
  // sigma默认0.5
  G1Predictions(double sigma) : _sigma(sigma) {
    assert(sigma >= 0.0, "Confidence must be larger than or equal to zero");
  }

  // 可信度系数
  double sigma() const { return _sigma; }

  double predict(TruncatedSeq const* seq) const {
    // davg(): 衰减平均值
    return seq->davg() + _sigma * stddev_estimate(seq);
  }
};
```

```cpp
///////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/utilities/numberSeq.cpp //
///////////////////////////////////////////////////////////////

/**
 * _num: 列表中元素的数量, 即列表长度
 * _davg: 衰减平均值
 * _dvariance: 衰减方差
 * _alpha: 默认值0.3
 */
AbsSeq::AbsSeq(double alpha) :
  _num(0), _sum(0.0), _sum_of_squares(0.0),
  _davg(0.0), _dvariance(0.0), _alpha(alpha) {
}

void AbsSeq::add(double val) {
  if (_num == 0) {
    // if the sequence is empty, the davg is the same as the value
    _davg = val;
    // and the variance is 0
    _dvariance = 0.0;
  } else {
    // otherwise, calculate both
    // Formula from "Incremental calculation of weighted mean and variance" by Tony Finch
    // diff := x - mean
    // incr := alpha * diff
    // mean := mean + incr
    // variance := (1 - alpha) * (variance + diff * incr)
    // PDF available at https://fanf2.user.srcf.net/hermes/doc/antiforgery/stats.pdf
    double diff = val - _davg;
    double incr = _alpha * diff;
    _davg += incr;
    _dvariance = (1.0 - _alpha) * (_dvariance + diff * incr);
  }
}
```

```cpp
///////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/utilities/numberSeq.cpp //
///////////////////////////////////////////////////////////////

double AbsSeq::dsd() const {
  double var = dvariance();
  guarantee( var >= 0.0, "variance should not be negative" );
  return sqrt(var);
}

double AbsSeq::dvariance() const {
  if (_num <= 1)
    return 0.0;

  double result = _dvariance;
  if (result < 0.0) {
    // due to loss-of-precision errors, the variance might be negative
    // by a small bit

    guarantee(-0.1 < result && result < 0.0,
               "if variance is negative, it should be very small");
    result = 0.0;
  }
  return result;
}
```
