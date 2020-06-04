include $(sort $(wildcard $(BR2_EXTERNAL_SNAKEWARE_PATH)/package/*/*.mk))

PYTHON3_CONF_OPTS += \
		     --with-lto \
		     --enable-optimizations
