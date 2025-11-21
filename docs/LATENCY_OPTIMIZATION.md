# 延迟优化报告 (Latency Optimization Report)

**版本**: 0.1.0
**日期**: 2025-11-21
**目标**: 将端到端延迟控制在 50-60ms (已达成)

---

## 1. 现状概览 (Current Status)

目前端到端延迟测量值稳定在 **50-60ms** 左右。

### 延迟构成
| 阶段 (Stage) | 耗时 (Time) | 备注 (Notes) |
|---|---|---|
| **AudioWorklet Buffer** | 23.2ms | 1024 samples @ 44.1kHz (用于保证 YIN 算法精度) |
| **Processing Overhead** | 5-10ms | YIN + FFT 计算 |
| **Message Passing** | 1-2ms | Worklet -> Main Thread |
| **Synthesis Smoothing** | 10-20ms | Tone.js rampTo & buffers |
| **System Output** | 10ms | 操作系统/浏览器底层缓冲 |
| **总计** | **~50-60ms** | 测量值匹配 ✓ |

---

## 2. 优化历程 (Optimization History)

### 阶段 1: 初始状态 (180ms+)
- 使用 ScriptProcessor (4096 buffer)
- Tone.js 默认 lookAhead (100ms)
- 主线程阻塞严重

### 阶段 2: 架构重构 (AudioWorklet)
- 迁移至 AudioWorklet
- 移除 ScriptProcessor
- **当前状态**: 稳定在 50-60ms

### 阶段 3: 关键配置 (Critical Config)

#### 1. 缓冲区大小 (Buffer Size)
在 `js/pitch-worklet.js` 中：
```javascript
// buffer size 1024 samples (~23ms)
// Necessary for accurate pitch detection > 80Hz
this.accumulationBuffer = new Float32Array(1024);
```

#### 2. Tone.js 零延迟调度
在 `js/continuous-synth.js` 中：
```javascript
// Remove 100ms scheduling latency
Tone.context.lookAhead = 0;
```

#### 3. AudioContext 模式
在 `js/audio-io.js` 中：
```javascript
const context = new AudioContext({
    latencyHint: 'interactive', // 浏览器会尝试使用最小缓冲
    sampleRate: 44100
});
```

---

## 3. 进一步优化空间 (Future Optimization)

如果要进一步降低延迟 (<30ms)，需要：
1.  **减小 Buffer**: 将 1024 降至 512 或 256。
    *   *代价*: 低频检测准确率下降 (80Hz -> 170Hz)。
2.  **WebAssembly**: 使用 WASM 重写 YIN 算法以提高处理速度。
3.  **原生合成**: 移除 Tone.js，直接使用 Web Audio API 节点以减少 overhead。
