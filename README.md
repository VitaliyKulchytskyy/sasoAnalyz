# .saso format
## Description
The saso stands for *Slices of Analog Stamp Optimized*. The idea behind this format is based on 
how to collect analog data. The data is collected into the allocated array whose size depends on
the maximum ADC value (e.g. 2^10, 2^12). Whenever an analog value is received it will increment
the index of the array, which is equal to the received value. This array is called a slice.
The array of the slices is called a record.
Except for slices this format also has two parameters: ```slicing_period``` and ```duration```.
The first one is the period of taking slices (in microseconds (mu)), and the second one is the duration (in milliseconds (ms)) of recording a .saso file.


## Implementation
To optimize a way to store data it doesn't allocate a whole array. Instead, it uses a ```value_t```. This
type has two fields: ```value``` and ```count```. The ```value``` is the index (or an analog value), and the ```count``` is how
many times the value was collected. The array of ```value_t``` is ```slice_t```. An array of the ```slice_t``` is ```record_t```.

## ImHex structure:
```rust
struct value_t {
    u32 value;
    u32 count;
};

struct slice_t {
    u32 valueNum;
    value_t values[valueNum];
};

struct record_t {
    u64 slicingPer;
    u32 durqation;
    u32 sliceNum;
    slice_t slices[sliceNum];
};
```

# .psaso format
## Description
The paso stands for *Pattern of a Slice Analog Stamp Optimized*. This format is similar to the saso format but
with one difference. It just contains one slice and the comment for this slice.

## ImHex structure:
```rust
struct value_t {
    u32 value;
    u32 count;
};

struct slice_t {
    u32 valueNum;
    value_t values[valueNum];
};

struct pattern_t {
  u32 commentLen;
  char comment[commentLen];
  slice_t slice;
};
```
