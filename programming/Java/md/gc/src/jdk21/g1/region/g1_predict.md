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
    // 预测Young GC时新生代所需region数
    return predictor->predict(&_young_only_seq);
  } else {
    // 预测Mixed GC时新生代所需region数
    return predictor->predict(&_mixed_seq);
  }
}
```

## 停顿预测模型

```cpp
///////////////////////////////////////////////////////////////
// jdk21-jdk-21-ga/src/hotspot/share/gc/g1/g1Predictions.hpp //
///////////////////////////////////////////////////////////////

class G1Predictions {
 private:
  // 估算抽样数据的标准差
  double stddev_estimate(TruncatedSeq const* seq) const {
    // dsd(): 衰减标准差
    double estimate = seq->dsd();
    // seq->num(): 抽样数据, seq中的元素数量
    int const samples = seq->num();
    // 抽样数据不足5个, 做单独处理
    if (samples < 5) {
      estimate = MAX2(seq->davg() * (5 - samples) / 2.0, estimate);
    }
    return estimate;
  }
 public:
  // 调用位置:
  // G1Policy::G1Policy(STWGCTimer* gc_timer) :
  //   _predictor(G1ConfidencePercent / 100.0),
  // }
  //
  // G1ConfidencePercent: 默认50
  // sigma默认0.5
  G1Predictions(double sigma) : _sigma(sigma) {
    assert(sigma >= 0.0, "Confidence must be larger than or equal to zero");
  }

  // 可信度系数
  double sigma() const {
    return _sigma;
  }

  double predict(TruncatedSeq const* seq) const {
    // davg(): 衰减平均值
    return seq->davg() + _sigma * stddev_estimate(seq);
  }
};
```

## 衰减平均值和衰减方差

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
    // 如果添加元素之前, 队列为空,
    // 则添加这个元素之后, 队列只有1个元素,
    // 它的平均值就是这个元素的值, 方差是0
    _davg = val;
    _dvariance = 0.0;
  } else {
    // 计算平均值和方差
    // diff := x - mean
    // incr := alpha * diff
    // mean := mean + incr
    // variance := (1 - alpha) * (variance + diff * incr)
    // 计算公式来自这篇论文:
    // "Incremental calculation of weighted mean and variance" by Tony Finch
    // PDF available at https://fanf2.user.srcf.net/hermes/doc/antiforgery/stats.pdf
    double diff = val - _davg;
    double incr = _alpha * diff;
    _davg += incr;
    _dvariance = (1.0 - _alpha) * (_dvariance + diff * incr);
  }
}
```

## 衰减标准差

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
    // 由于double的精度损失, _dvariance有可能小于0
    guarantee(-0.1 < result && result < 0.0,
               "if variance is negative, it should be very small");
    result = 0.0;
  }
  return result;
}
```
