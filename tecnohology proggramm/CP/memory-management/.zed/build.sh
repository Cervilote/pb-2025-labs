#!/usr/bin/env bash
set -e

# ============================================================
# Параметры компиляции
# ============================================================

CFLAGS=(
    # -std=c17
    # -Wall
    # -Wextra
    # -g
    # -O0
    # -fsanitize=address
)

CXXFLAGS=(
    # -std=c++20
    # -Wall
    # -Wextra
    # -g
    # -O0
    -std=c++17
    # -fsanitize=address
)

RUSTFLAGS=(
    # -g
    # -C
    # opt-level=0
)

# ============================================================
# Не менять ниже этого места
# ============================================================

mkdir -p "$ZED_WORKTREE_ROOT/.zed/bin"

case "$ZED_FILE" in

    *.c)
        OUTPUT="$ZED_WORKTREE_ROOT/.zed/bin/$ZED_STEM"
        echo "=== C ==="
        echo "gcc ${CFLAGS[*]} $ZED_FILE"
        gcc "${CFLAGS[@]}" "$ZED_FILE" -o "$OUTPUT"
        echo
        echo "Built: $OUTPUT"
        ;;

    *.cpp|*.cc|*.cxx)
        OUTPUT="$ZED_WORKTREE_ROOT/.zed/bin/$ZED_STEM"
        echo "=== C++ ==="
        echo "g++ ${CXXFLAGS[*]} $ZED_FILE"
        g++ "${CXXFLAGS[@]}" "$ZED_FILE" -o "$OUTPUT"
        echo
        echo "Built: $OUTPUT"
        ;;

    *.rs)
        OUTPUT="$ZED_WORKTREE_ROOT/.zed/bin/$ZED_STEM"
        echo "=== Rust ==="
        echo "rustc ${RUSTFLAGS[*]} $ZED_FILE"
        rustc "${RUSTFLAGS[@]}" "$ZED_FILE" -o "$OUTPUT"
        echo
        echo "Built: $OUTPUT"
        ;;

    *)
        echo "ERROR: unsupported file type:"
        echo "$ZED_FILE"
        exit 1
        ;;
esac
