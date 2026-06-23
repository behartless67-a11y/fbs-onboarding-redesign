#!/usr/bin/env bash

set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
LLAMA_SERVER_BIN_DEFAULT="/media/scratch/llm/llama.cpp/build/bin/llama-server"
MODEL_ROOT_DEFAULT="/media/annex/llama_cpp/models"
MODEL_DEFAULT_BASENAME="mistral-7b-instruct-v0.2.Q4_K_M.gguf"

resolve_model_name() {
  local model_root="$1"
  local model_arg="$2"

  case "$model_arg" in
    gpt-oss|gptoss)
      printf "%s/%s\n" "$model_root" "gpt-oss-20b-Q5_K_M.gguf"
      ;;
    gpt-oss-q4|gptoss-q4)
      printf "%s/%s\n" "$model_root" "gpt-oss-20b-Q4_K_M.gguf"
      ;;
    mistral)
      printf "%s/%s\n" "$model_root" "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
      ;;
    mistral-small)
      printf "%s/%s\n" "$model_root" "Mistral-Small-3.2-24B-Instruct-2506-Q4_K_M.gguf"
      ;;
    gemma|gemma-7b)
      printf "%s/%s\n" "$model_root" "gemma-7b.gguf"
      ;;
    *)
      printf "%s\n" "$model_arg"
      ;;
  esac
}

cpu_count="$(nproc 2>/dev/null || echo 4)"
default_threads=$((cpu_count - 2))
if (( default_threads < 1 )); then
  default_threads=1
fi

LLAMA_SERVER_BIN="${LLAMA_SERVER_BIN:-$LLAMA_SERVER_BIN_DEFAULT}"
MODEL_ROOT="${MODEL_ROOT:-$MODEL_ROOT_DEFAULT}"
MODEL="${MODEL:-$MODEL_DEFAULT_BASENAME}"

if [[ $# -gt 0 && "${1:-}" != "--" && "${1:0:1}" != "-" ]]; then
  MODEL="$1"
  shift
fi

if [[ "${1:-}" == "--" ]]; then
  shift
fi

BIND_HOST="${LLAMA_HOST:-${BIND_HOST:-127.0.0.1}}"
BIND_PORT="${LLAMA_PORT:-${PORT:-8080}}"
ALIAS="${ALIAS:-agco-lesotho}"
CTX_SIZE="${CTX_SIZE:-12288}"
THREADS="${THREADS:-$default_threads}"
THREADS_BATCH="${THREADS_BATCH:-$THREADS}"
THREADS_HTTP="${THREADS_HTTP:-2}"
BATCH_SIZE="${BATCH_SIZE:-2048}"
UBATCH_SIZE="${UBATCH_SIZE:-512}"
N_PARALLEL="${N_PARALLEL:-1}"
N_PREDICT="${N_PREDICT:-1024}"
TEMP="${TEMP:-0.2}"
TOP_P="${TOP_P:-0.9}"
REPEAT_PENALTY="${REPEAT_PENALTY:-1.05}"
CACHE_REUSE="${CACHE_REUSE:-512}"
GPU_LAYERS="${GPU_LAYERS:--1}"
REASONING_BUDGET="${REASONING_BUDGET:-0}"

MODEL="$(resolve_model_name "$MODEL_ROOT" "$MODEL")"
if [[ ! -f "$MODEL" ]]; then
  MODEL="$MODEL_ROOT/$MODEL"
fi

if [[ ! -x "$LLAMA_SERVER_BIN" ]]; then
  echo "llama-server not found or not executable: $LLAMA_SERVER_BIN" >&2
  exit 1
fi

if [[ ! -f "$MODEL" ]]; then
  echo "Model file not found: $MODEL" >&2
  exit 1
fi

gpu_args=()
if [[ "$GPU_LAYERS" == "0" ]]; then
  gpu_args=(--device none --gpu-layers 0)
else
  gpu_args=(--gpu-layers "$GPU_LAYERS")
fi

echo "Starting llama-server"
echo "  bin:     $LLAMA_SERVER_BIN"
echo "  model:   $MODEL"
echo "  alias:   $ALIAS"
echo "  listen:  http://$BIND_HOST:$BIND_PORT"
echo "  threads: $THREADS (batch: $THREADS_BATCH, http: $THREADS_HTTP)"
echo "  ctx:     $CTX_SIZE"
echo "  gpu:     $GPU_LAYERS layers"
echo "  think:   reasoning budget $REASONING_BUDGET"
echo

if [[ -n "${HOST:-}" && -z "${LLAMA_HOST:-}" && "$BIND_HOST" == "127.0.0.1" ]]; then
  echo "  note:    ignoring HOST=$HOST from the shell environment; use LLAMA_HOST to override bind address"
  echo
fi

exec "$LLAMA_SERVER_BIN" \
  --model "$MODEL" \
  --alias "$ALIAS" \
  --host "$BIND_HOST" \
  --port "$BIND_PORT" \
  --ctx-size "$CTX_SIZE" \
  --threads "$THREADS" \
  --threads-batch "$THREADS_BATCH" \
  --threads-http "$THREADS_HTTP" \
  --batch-size "$BATCH_SIZE" \
  --ubatch-size "$UBATCH_SIZE" \
  --parallel "$N_PARALLEL" \
  --n-predict "$N_PREDICT" \
  --temp "$TEMP" \
  --top-p "$TOP_P" \
  --repeat-penalty "$REPEAT_PENALTY" \
  --cache-reuse "$CACHE_REUSE" \
  --reasoning-budget "$REASONING_BUDGET" \
  --jinja \
  --no-webui \
  "${gpu_args[@]}" \
  "$@"
